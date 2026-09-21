"""WebSocket support for real-time updates."""
import json
import asyncio
from typing import Any, Callable, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class MessageType(str, Enum):
    """WebSocket message types."""
    STATE_UPDATE = "state_update"
    EVENT = "event"
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    PING = "ping"
    PONG = "pong"


@dataclass
class Message:
    """WebSocket message."""
    type: MessageType
    data: Dict[str, Any]
    client_id: Optional[str] = None


class WebSocketServer:
    """Simple WebSocket server for real-time communication."""
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Dict[str, Any] = {}
        self.handlers: Dict[MessageType, Callable] = {}
        self._running = False
    
    def on(self, message_type: MessageType, handler: Callable):
        """Register a message handler."""
        self.handlers[message_type] = handler
    
    async def start(self):
        """Start the WebSocket server."""
        try:
            import websockets
        except ImportError:
            print("[ontaic] websockets not installed. Run: pip install websockets")
            return
        
        self._running = True
        
        async def handler(websocket, path):
            client_id = str(id(websocket))
            self.clients[client_id] = websocket
            print(f"[ontaic-ws] Client connected: {client_id}")
            
            try:
                # Send connect message
                await self._send(websocket, Message(
                    type=MessageType.CONNECT,
                    data={"client_id": client_id}
                ))
                
                async for message in websocket:
                    try:
                        msg = json.loads(message)
                        msg_type = MessageType(msg.get("type", "event"))
                        
                        # Call handler if registered
                        if msg_type in self.handlers:
                            await self.handlers[msg_type](client_id, msg.get("data", {}))
                        
                    except json.JSONDecodeError:
                        print(f"[ontaic-ws] Invalid JSON: {message}")
                        
            except websockets.exceptions.ConnectionClosed:
                pass
            finally:
                del self.clients[client_id]
                print(f"[ontaic-ws] Client disconnected: {client_id}")
        
        async with websockets.serve(handler, self.host, self.port):
            print(f"[ontaic-ws] Server started on ws://{self.host}:{self.port}")
            await asyncio.Future()  # Run forever
    
    async def _send(self, websocket, message: Message):
        """Send a message to a websocket."""
        data = {
            "type": message.type.value,
            "data": message.data,
        }
        if message.client_id:
            data["client_id"] = message.client_id
        await websocket.send(json.dumps(data))
    
    async def broadcast(self, message: Message):
        """Broadcast a message to all connected clients."""
        if not self.clients:
            return
        
        for client_id, websocket in list(self.clients.items()):
            try:
                await self._send(websocket, message)
            except Exception as e:
                print(f"[ontaic-ws] Error sending to {client_id}: {e}")
    
    async def send_to(self, client_id: str, message: Message):
        """Send a message to a specific client."""
        if client_id in self.clients:
            await self._send(self.clients[client_id], message)
    
    def stop(self):
        """Stop the WebSocket server."""
        self._running = False


class WebSocketClient:
    """WebSocket client for browser-side real-time updates."""
    
    def __init__(self, url: str = "ws://localhost:8765"):
        self.url = url
        self.handlers: Dict[str, Callable] = {}
        self._connected = False
        self._ws = None
    
    def on(self, event: str, handler: Callable):
        """Register an event handler."""
        self.handlers[event] = handler
    
    async def connect(self):
        """Connect to the WebSocket server."""
        try:
            import websockets
        except ImportError:
            print("[ontaic] websockets not installed. Run: pip install websockets")
            return
        
        async with websockets.connect(self.url) as ws:
            self._ws = ws
            self._connected = True
            print(f"[ontaic-ws] Connected to {self.url}")
            
            # Send connect message
            await self._send(MessageType.CONNECT, {})
            
            # Listen for messages
            async for message in ws:
                try:
                    msg = json.loads(message)
                    msg_type = msg.get("type", "")
                    
                    if msg_type in self.handlers:
                        await self.handlers[msg_type](msg.get("data", {}))
                        
                except json.JSONDecodeError:
                    print(f"[ontaic-ws] Invalid JSON: {message}")
    
    async def _send(self, msg_type: MessageType, data: Dict):
        """Send a message to the server."""
        if self._ws:
            message = {
                "type": msg_type.value,
                "data": data,
            }
            await self._ws.send(json.dumps(message))
    
    async def send_state_update(self, state: Dict):
        """Send a state update to the server."""
        await self._send(MessageType.STATE_UPDATE, {"state": state})
    
    async def send_event(self, event_name: str, data: Dict):
        """Send an event to the server."""
        await self._send(MessageType.EVENT, {"event": event_name, **data})
    
    def disconnect(self):
        """Disconnect from the server."""
        self._connected = False
        if self._ws:
            self._ws.close()


# Server-side state manager with WebSocket sync
class RealtimeState:
    """State that syncs across clients via WebSocket."""
    
    def __init__(self, ws_server: WebSocketServer):
        self.ws_server = ws_server
        self.state: Dict[str, Any] = {}
        self.clients_state: Dict[str, Dict[str, Any]] = {}
    
    async def set(self, key: str, value: Any, broadcast: bool = True):
        """Set a state value."""
        self.state[key] = value
        
        if broadcast:
            await self.ws_server.broadcast(Message(
                type=MessageType.STATE_UPDATE,
                data={"key": key, "value": value}
            ))
    
    async def get(self, key: str, default: Any = None) -> Any:
        """Get a state value."""
        return self.state.get(key, default)
    
    async def update(self, updates: Dict[str, Any], broadcast: bool = True):
        """Update multiple state values."""
        self.state.update(updates)
        
        if broadcast:
            await self.ws_server.broadcast(Message(
                type=MessageType.STATE_UPDATE,
                data={"state": updates}
            ))
    
    def set_client_state(self, client_id: str, state: Dict[str, Any]):
        """Set state for a specific client."""
        self.clients_state[client_id] = state
    
    def get_client_state(self, client_id: str) -> Dict[str, Any]:
        """Get state for a specific client."""
        return self.clients_state.get(client_id, {})
