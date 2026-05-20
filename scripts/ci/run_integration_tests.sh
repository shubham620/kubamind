#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$ROOT_DIR"

mkdir -p build/artifacts

echo "1) Wait for backend API readiness"
./scripts/ci/health_check.sh http://localhost:8000/api/health 120

echo "2) Ingest logs into Qdrant"
python -m backend.app.ingest.qdrant_ingest --source simulations --collection logs || true

echo "3) Run predictive training wrapper (if data available)"
python backend/app/predictive/train_wrapper.py || true

echo "4) Run failure simulator in background"
python simulations/failure_simulator.py &
SIM_PID=$!
echo "Simulator PID: $SIM_PID"

echo "5) Allow agents to process (sleeping 20s)"
sleep 20

echo "6) Query anomalies endpoint"
curl -sS http://localhost:8000/api/insights/anomalies -o build/artifacts/anomalies.json || true

echo "7) Run RAG query"
python -m backend.app.llm.rag --q "Why is payment-service slow?" > build/artifacts/rag_answer.txt || true

echo "8) Run backend pytest unit/integration tests"
pip install -r backend/requirements.txt || true
pytest -q backend -k "not longrunning" --maxfail=1 || true

echo "9) Frontend: install and build"
if [ -d frontend ]; then
  pushd frontend
  npm ci --silent || true
  npm run build --silent || true
  popd
fi

echo "10) WebSocket smoke test"
python - <<'PY'
import asyncio, websockets
async def test():
    uri = 'ws://localhost:8000/api/chat/ws'
    try:
        async with websockets.connect(uri) as ws:
            await ws.send('{"message":"health_check"}')
            resp = await ws.recv()
            print('WS response:', resp[:200])
    except Exception as e:
        print('WS test failed:', e)
asyncio.run(test())
PY

echo "11) Capture some container logs"
docker compose ps --services | xargs -I {} sh -c 'docker compose logs --tail 200 {} > build/artifacts/{}.log || true'

echo "12) Stop simulator"
kill $SIM_PID || true

echo "Integration tests finished"
