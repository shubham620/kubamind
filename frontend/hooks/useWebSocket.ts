import { useEffect, useRef, useState } from 'react';
import { WebSocketClient } from '@/lib/websocket';

export function useWebSocket(url: string) {
  const clientRef = useRef<WebSocketClient | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const client = new WebSocketClient(url);
    clientRef.current = client;

    client.on('connected', () => setIsConnected(true));
    client.on('disconnected', () => setIsConnected(false));
    client.on('message', (data) => setData(data));

    client.connect().catch(console.error);

    return () => {
      client.close();
    };
  }, [url]);

  const send = (data: any) => {
    if (clientRef.current) {
      clientRef.current.send(data);
    }
  };

  return { isConnected, data, send };
}
