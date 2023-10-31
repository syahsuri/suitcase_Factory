// Define WebSocket URLs
const serverSocketUrl = "ws://localhost:8080";
const robotSocketUrl = "ws://localhost:1080";

// WebSocket for server communication
const serverSocket = new WebSocket(serverSocketUrl);
const robotSocket = new WebSocket(robotSocketUrl);

function serverSocket() {
  serverSocket.addEventListener("open", () => {
    console.log("WebSocket connection to server established.");
  });

  serverSocket.addEventListener("close", () => {
    console.log("WebSocket connection to server closed.");
  });

  serverSocket.addEventListener("error", (error) => {
    console.error("WebSocket error to server:", error);
  });
}

// WebSocket for robot communication
function robotSocket() {
  robotSocket.addEventListener("open", () => {
    console.log("WebSocket connection to robot established.");
  });

  robotSocket.addEventListener("close", () => {
    console.log("WebSocket connection to robot closed.");
  });

  robotSocket.addEventListener("error", (error) => {
    console.error("WebSocket error to robot:", error);
  });
}

// Define functions for different actions
function connectWebSocket() {
  robotSocket();
}

connectWebSocket();

function toggleFrameInput(checkbox) {
  // Implementation for toggling frame input
  // ...
}

function submitFrames() {
  // Implementation for submitting frames
  // ...
}

function resetFrames() {
  // Implementation for resetting frames
  // ...
}

function startFrames() {
  // Implementation for starting frames
  // ...
}

function stopFrames() {
  // Implementation for stopping frames
  // ...
}

function pause() {
  // Implementation for pausing
  // ...
}

function play() {
  // Implementation for playing
  // ...
}

function stop() {
  // Implementation for stopping
  // ...
}

function updateInterface(data) {
  // Implementation for updating the interface
  // ...
}

function status() {
  // Implementation for updating the status
  // ...
}

function back() {
  // Implementation for going back
  // ...
}

// Other utility functions

function validateNonNegativeInput(inputId) {
  // Implementation for input validation
  // ...
}

function showModal() {
  // Implementation for showing the modal
  // ...
}

// Event listeners and UI interactions

// ...
