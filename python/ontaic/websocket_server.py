"""WebSocket server integration for ontaic."""
import asyncio
import json
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import threading


@dataclass
class Client:
    """WebSocket client."""
    id: str
    websocket: Any
    connected_at: str
    last_seen: str
    data: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.data is None:
            self.data = {}


@dataclass
class Room:
    """WebSocket room for grouping clients."""
    name: str
    clients: Dict[str, Client] = None
    created_at: str = ""
    
    def __post_init__(self):
        if self.clients is None:
            self.clients = {}
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def add_client(self, client: Client):
        self.clients[client.id] = client
    
    def remove_client(self, client_id: str):
        self.clients.pop(client_id, None)
    
    def broadcast(self, message: Dict[str, Any], exclude: str = None):
        """Broadcast message to all clients in the room."""
        for client_id, client in list(self.clients.items()):
            if client_id != exclude:
                try:
                    asyncio.create_task(self._send(client.websocket, message))
                except Exception:
                    pass
    
    async def _send(self, websocket, message: Dict[str, Any]):
        await websocket.send(json.dumps(message))


class WebSocketServer:
    """WebSocket server for real-time communication."""
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Dict[str, Client] = {}
        self.rooms: Dict[str, Room] = {}
        self.handlers: Dict[str, Callable] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None
    
    def on(self, event: str, handler: Callable):
        """Register an event handler."""
        self.handlers[event] = handler
    
    def emit(self, client_id: str, event: str, data: Dict[str, Any]):
        """Send an event to a specific client."""
        if client_id in self.clients:
            client = self.clients[client_id]
            message = {"event": event, "data": data, "timestamp": datetime.now().isoformat()}
            asyncio.create_task(self._send(client.websocket, message))
    
    def broadcast(self, event: str, data: Dict[str, Any], room: str = None):
        """Broadcast an event to all clients or a specific room."""
        message = {"event": event, "data": data, "timestamp": datetime.now().isoformat()}
        
        if room and room in self.rooms:
            self.rooms[room].broadcast(message)
        else:
            for client_id, client in list(self.clients.items()):
                try:
                    asyncio.create_task(self._send(client.websocket, message))
                except Exception:
                    pass
    
    def join_room(self, client_id: str, room_name: str):
        """Add a client to a room."""
        if room_name not in self.rooms:
            self.rooms[room_name] = Room(name=room_name)
        
        if client_id in self.clients:
            self.rooms[room_name].add_client(self.clients[client_id])
    
    def leave_room(self, client_id: str, room_name: str):
        """Remove a client from a room."""
        if room_name in self.rooms:
            self.rooms[room_name].remove_client(client_id)
    
    def get_room_clients(self, room_name: str) -> List[str]:
        """Get all client IDs in a room."""
        if room_name in self.rooms:
            return list(self.rooms[room_name].clients.keys())
        return []
    
    def get_client_count(self) -> int:
        """Get the number of connected clients."""
        return len(self.clients)
    
    def get_room_count(self) -> int:
        """Get the number of rooms."""
        return len(self.rooms)
    
    async def _send(self, websocket, message: Dict[str, Any]):
        """Send a message to a websocket."""
        try:
            await websocket.send(json.dumps(message))
        except Exception:
            pass
    
    def start(self):
        """Start the WebSocket server in a separate thread."""
        self._running = True
        self._thread = threading.Thread(target=self._run_server, daemon=True)
        self._thread.start()
        print(f"[ontaic-ws] Server started on ws://{self.host}:{self.port}")
    
    def _run_server(self):
        """Run the WebSocket server."""
        try:
            import websockets
            asyncio.run(self._start_server())
        except ImportError:
            print("[ontaic] websockets not installed. Run: pip install websockets")
        except Exception as e:
            print(f"[ontaic-ws] Server error: {e}")
    
    async def _start_server(self):
        """Start the WebSocket server asynchronously."""
        import websockets
        
        async def handler(websocket, path):
            client_id = str(id(websocket))
            client = Client(
                id=client_id,
                websocket=websocket,
                connected_at=datetime.now().isoformat(),
                last_seen=datetime.now().isoformat(),
            )
            self.clients[client_id] = client
            print(f"[ontaic-ws] Client connected: {client_id}")
            
            # Send connect event
            await self._send(websocket, {
                "event": "connect",
                "data": {"client_id": client_id},
                "timestamp": datetime.now().isoformat(),
            })
            
            # Call connect handler
            if "connect" in self.handlers:
                self.handlers["connect"](client_id, {})
            
            try:
                async for message in websocket:
                    try:
                        msg = json.loads(message)
                        event = msg.get("event", "")
                        data = msg.get("data", {})
                        
                        # Update last seen
                        client.last_seen = datetime.now().isoformat()
                        
                        # Call handler if registered
                        if event in self.handlers:
                            self.handlers[event](client_id, data)
                        
                        # Handle built-in events
                        if event == "join_room":
                            room_name = data.get("room", "")
                            if room_name:
                                self.join_room(client_id, room_name)
                                await self._send(websocket, {
                                    "event": "room_joined",
                                    "data": {"room": room_name},
                                    "timestamp": datetime.now().isoformat(),
                                })
                        
                        elif event == "leave_room":
                            room_name = data.get("room", "")
                            if room_name:
                                self.leave_room(client_id, room_name)
                                await self._send(websocket, {
                                    "event": "room_left",
                                    "data": {"room": room_name},
                                    "timestamp": datetime.now().isoformat(),
                                })
                        
                        elif event == "ping":
                            await self._send(websocket, {
                                "event": "pong",
                                "data": {},
                                "timestamp": datetime.now().isoformat(),
                            })
                        
                    except json.JSONDecodeError:
                        print(f"[ontaic-ws] Invalid JSON: {message}")
                        
            except Exception as e:
                print(f"[ontaic-ws] Client error: {e}")
            finally:
                # Remove client from all rooms
                for room_name in list(self.rooms.keys()):
                    self.leave_room(client_id, room_name)
                
                # Remove client
                del self.clients[client_id]
                print(f"[ontaic-ws] Client disconnected: {client_id}")
                
                # Call disconnect handler
                if "disconnect" in self.handlers:
                    self.handlers["disconnect"](client_id, {})
        
        async with websockets.serve(handler, self.host, self.port):
            await asyncio.Future()  # Run forever
    
    def stop(self):
        """Stop the WebSocket server."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
        print("[ontaic-ws] Server stopped")


class WebSocketClient:
    """WebSocket client for connecting to a server."""
    
    def __init__(self, url: str = "ws://localhost:8765"):
        self.url = url
        self.handlers: Dict[str, Callable] = {}
        self._connected = False
        self._ws = None
        self._thread: Optional[threading.Thread] = None
    
    def on(self, event: str, handler: Callable):
        """Register an event handler."""
        self.handlers[event] = handler
    
    def connect(self):
        """Connect to the WebSocket server."""
        self._connected = True
        self._thread = threading.Thread(target=self._run_client, daemon=True)
        self._thread.start()
        print(f"[ontaic-ws] Connecting to {self.url}")
    
    def _run_client(self):
        """Run the WebSocket client."""
        try:
            import websockets
            asyncio.run(self._start_client())
        except ImportError:
            print("[ontaic] websockets not installed. Run: pip install websockets")
        except Exception as e:
            print(f"[ontaic-ws] Client error: {e}")
    
    async def _start_client(self):
        """Start the WebSocket client asynchronously."""
        import websockets
        
        async with websockets.connect(self.url) as ws:
            self._ws = ws
            self._connected = True
            print(f"[ontaic-ws] Connected to {self.url}")
            
            # Call connect handler
            if "connect" in self.handlers:
                self.handlers["connect"]({})
            
            try:
                async for message in ws:
                    try:
                        msg = json.loads(message)
                        event = msg.get("event", "")
                        data = msg.get("data", {})
                        
                        # Call handler if registered
                        if event in self.handlers:
                            self.handlers[event](data)
                        
                    except json.JSONDecodeError:
                        print(f"[ontaic-ws] Invalid JSON: {message}")
                        
            except Exception as e:
                print(f"[ontaic-ws] Connection error: {e}")
            finally:
                self._connected = False
                # Call disconnect handler
                if "disconnect" in self.handlers:
                    self.handlers["disconnect"]({})
    
    def emit(self, event: str, data: Dict[str, Any]):
        """Send an event to the server."""
        if self._ws and self._connected:
            message = {"event": event, "data": data, "timestamp": datetime.now().isoformat()}
            asyncio.create_task(self._ws.send(json.dumps(message)))
    
    def join_room(self, room_name: str):
        """Join a room."""
        self.emit("join_room", {"room": room_name})
    
    def leave_room(self, room_name: str):
        """Leave a room."""
        self.emit("leave_room", {"room": room_name})
    
    def disconnect(self):
        """Disconnect from the server."""
        self._connected = False
        if self._ws:
            self._ws.close()
        print(f"[ontaic-ws] Disconnected from {self.url}")


# JavaScript code for WebSocket client
def generate_ws_js_code() -> str:
    """Generate JavaScript code for WebSocket client."""
    return """
    // WebSocket Client
    const wsClient = {
        ws: null,
        url: 'ws://localhost:8765',
        handlers: {},
        reconnectAttempts: 0,
        maxReconnectAttempts: 5,
        reconnectDelay: 1000,
        
        connect(url) {
            this.url = url || this.url;
            this.ws = new WebSocket(this.url);
            
            this.ws.onopen = () => {
                console.log('[ws] Connected to', this.url);
                this.reconnectAttempts = 0;
                this.emit('connect', {});
            };
            
            this.ws.onmessage = (event) => {
                try {
                    const msg = JSON.parse(event.data);
                    const { event: eventName, data } = msg;
                    
                    if (this.handlers[eventName]) {
                        this.handlers[eventName](data);
                    }
                } catch (e) {
                    console.error('[ws] Invalid message:', e);
                }
            };
            
            this.ws.onclose = () => {
                console.log('[ws] Disconnected');
                this.emit('disconnect', {});
                this.tryReconnect();
            };
            
            this.ws.onerror = (error) => {
                console.error('[ws] Error:', error);
            };
        },
        
        tryReconnect() {
            if (this.reconnectAttempts < this.maxReconnectAttempts) {
                this.reconnectAttempts++;
                console.log(`[ws] Reconnecting in ${this.reconnectDelay}ms (attempt ${this.reconnectAttempts})`);
                setTimeout(() => this.connect(), this.reconnectDelay);
            }
        },
        
        on(event, handler) {
            this.handlers[event] = handler;
        },
        
        emit(event, data) {
            if (this.ws && this.ws.readyState === WebSocket.OPEN) {
                this.ws.send(JSON.stringify({
                    event,
                    data,
                    timestamp: new Date().toISOString()
                }));
            }
        },
        
        joinRoom(room) {
            this.emit('join_room', { room });
        },
        
        leaveRoom(room) {
            this.emit('leave_room', { room });
        },
        
        disconnect() {
            if (this.ws) {
                this.ws.close();
            }
        }
    };
    """


# Example usage
def create_ws_example():
    """Create an example WebSocket setup."""
    server = WebSocketServer(host="localhost", port=8765)
    
    # Register handlers
    @server.on("connect")
    def handle_connect(client_id, data):
        print(f"Client {client_id} connected")
        server.broadcast("user_joined", {"client_id": client_id})
    
    @server.on("disconnect")
    def handle_disconnect(client_id, data):
        print(f"Client {client_id} disconnected")
        server.broadcast("user_left", {"client_id": client_id})
    
    @server.on("chat_message")
    def handle_chat_message(client_id, data):
        message = data.get("message", "")
        room = data.get("room", "general")
        server.broadcast("chat_message", {
            "client_id": client_id,
            "message": message,
        }, room=room)
    
    return server
