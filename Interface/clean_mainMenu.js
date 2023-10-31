let serverSocket;
let robotSocket;

document.getElementById("startBtn").addEventListener("click", function (event) {
  event.preventDefault(); // Prevent the default behavior (navigation)
  powerButton();
});

function createWebSocket(url, onMessageCallback) {
  const socket = new WebSocket(url);

  socket.addEventListener("open", () => {
    console.log(`WebSocket connected to ${url}`);
  });

  socket.addEventListener("message", (event) => {
    console.log(`Received from ${url}: ${event.data}`);
    onMessageCallback(event.data);
  });

  socket.addEventListener("close", () => {
    console.log(`WebSocket connection to ${url} closed`);
  });

  return socket;
}

function on() {
  robotSocket = createWebSocket("ws://localhost:1080", (data) => {
    // Process the received data from robot
  });

  // Send initial messages
  const messages = ["power on\r\n", "safetystatus\r\n", "brake release\r\n"];
  messages.forEach((message) => robotSocket.send(message));
}

function connectWebSocket() {
  serverSocket = createWebSocket("ws://localhost:8080", (data) => {
    // Process the received data from server.js
  });

  // Send a specific message (e.g., "3") upon connection
  serverSocket.send("3");
}

function powerButton() {
  const serverSocket = createWebSocket("ws://localhost:8080", (data) => {
    console.log("Check2");
    // Process the received data from server.js
  });

  // Send "ready" message and navigate to another page
  serverSocket.send("ready");
  window.location.href = "insertframe.html";
}

function refillButton() {
  // Show a confirmation dialog
  Swal.fire({
    title: "Warning! Robot is moving!",
    icon: "warning",
    confirmButtonText: "Glue disposal",
    allowOutsideClick: false,
    willOpen: () => {
      Swal.showLoading();
    },
  }).then((result) => {
    if (result.isConfirmed) {
      const serverSocket = createWebSocket("ws://localhost:8080", (data) => {
        // Process the received data from server.js
      });

      // Send "dispose" message and show another confirmation dialog
      serverSocket.send("dispose");
      Swal.fire({
        title: "Warning! Please clean nozzle",
        icon: "warning",
        confirmButtonText: "Continue",
        allowOutsideClick: false,
        willOpen: () => {
          Swal.showLoading();
        },
      });
    }
  });

  // Establish a WebSocket connection to the server.js
  const serverSocket = createWebSocket("ws://localhost:8080", (data) => {
    // Process the received data from server.js
  });

  // Send "inspect" message
  serverSocket.send("inspect");
}

function stopButton() {
  // Show a confirmation dialog
  Swal.fire({
    title: "Shutdown robot",
    icon: "info",
    confirmButtonText: "Ok",
    allowOutsideClick: false,
    willOpen: () => {
      Swal.showLoading();
    },
  }).then((result) => {
    if (result.isConfirmed) {
      // The user clicked "OK," so you can perform further actions if needed
    }
  });

  const serverSocket = createWebSocket("ws://localhost:8080", (data) => {
    // Process the received data from server.js
  });

  // Send "stop" message
  serverSocket.send("stop");
}

function dispose() {
  // Show a confirmation dialog
  Swal.fire({
    title: "Warning! Robot is moving!",
    icon: "warning",
    confirmButtonText: "Continue",
    allowOutsideClick: false,
    willOpen: () => {
      Swal.showLoading();
    },
  }).then((result) => {
    if (result.isConfirmed) {
      // The user clicked "OK," so you can perform further actions if needed
    }
  });

  const serverSocket = createWebSocket("ws://localhost:8080", (data) => {
    // Process the received data from server.js
  });

  // Send "dispose" message
  serverSocket.send("dispose");
}

// Connect to WebSocket when the page loads
connectWebSocket();
