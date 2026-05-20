"""
WebSocket routes for real-time updates
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
import json
import logging
from app.websocket_manager import manager

logger = logging.getLogger(__name__)
router = APIRouter()


@router.websocket("/ws/analysis")
async def websocket_analysis_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time analysis updates"""
    await manager.connect(websocket)
    await manager.subscribe(websocket, "analysis")
    
    try:
        # Keep connection alive and listen for messages
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                
                if message.get("type") == "subscribe":
                    await manager.subscribe(websocket, message.get("channel", "analysis"))
                    await manager.send_personal(websocket, {
                        "type": "subscribed",
                        "channel": message.get("channel", "analysis")
                    })
                elif message.get("type") == "unsubscribe":
                    await manager.unsubscribe(websocket, message.get("channel", "analysis"))
                elif message.get("type") == "ping":
                    await manager.send_personal(websocket, {"type": "pong"})
                    
            except json.JSONDecodeError:
                await manager.send_personal(websocket, {
                    "type": "error",
                    "message": "Invalid JSON"
                })
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        logger.info("Client disconnected from analysis updates")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await manager.disconnect(websocket)


@router.websocket("/ws/metrics")
async def websocket_metrics_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time metrics"""
    await manager.connect(websocket)
    await manager.subscribe(websocket, "metrics")
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "ping":
                await manager.send_personal(websocket, {"type": "pong"})
                
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket metrics error: {e}")
        await manager.disconnect(websocket)


@router.websocket("/ws/alerts")
async def websocket_alerts_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time alerts"""
    await manager.connect(websocket)
    await manager.subscribe(websocket, "alerts")
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "ping":
                await manager.send_personal(websocket, {"type": "pong"})
                
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket alerts error: {e}")
        await manager.disconnect(websocket)
