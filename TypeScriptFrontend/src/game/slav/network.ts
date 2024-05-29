const ws = new WebSocket("ws://localhost:8765");

ws.onopen = () => {
  console.log("Connected to server");
  ws.send("Hello, server!");
};

ws.onmessage = (event) => {
  console.log("Received:", event.data);
};

ws.onerror = (error) => {
  console.log("WebSocket error:", error);
};

ws.onclose = () => {
  console.log("Disconnected from server");
};
