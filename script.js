 const socket = new WebSocket('ws://localhost:8080');

    socket.addEventListener('open', (event) => {
      console.log('Connected to server');
    });

    socket.addEventListener('message', (event) => {
      const messages = document.getElementById('messages');
      const li = document.createElement('li');
      li.textContent = 'Server: ' + event.data;
      messages.appendChild(li);
    });

    socket.addEventListener('close', (event) => {
      console.log('Connection closed');
    });

function sendFrameValues(frameValues) {
  if (websocket.readyState === WebSocket.OPEN) {
    websocket.send(
      JSON.stringify({
        type: "frameValues",
        values: frameValues,
      })
    );
  }
}

function sendProgramStartedMessage() {
  if (websocket.readyState === WebSocket.OPEN) {
    websocket.send(
      JSON.stringify({
        type: "start",
      })
    );
  }
}

function toggleButton() {
  const toggleButton = document.getElementById("toggleButton");
  const additionalButtonsDiv = document.getElementById("additionalButtons");
  const infoDiv = document.getElementById("info");
  const startButton = document.getElementById("startButton");
  const resetButton = document.getElementById("resetButton");

  if (toggleButton.innerText === "ON") {
    toggleButton.innerText = "OFF";
    toggleButton.classList.remove("btn-primary");
    toggleButton.classList.add("btn-secondary");
    additionalButtonsDiv.style.display = "block";
    startButton.style.display = "none";
    localStorage.setItem("buttonState", "off");
    resetButton.style.marginLeft = "10px"; // Adjust the margin when ON/Off button text changes
  } else {
    toggleButton.innerText = "ON";
    toggleButton.classList.remove("btn-secondary");
    toggleButton.classList.add("btn-primary");
    additionalButtonsDiv.style.display = "none";
    startButton.style.display = "block";
    localStorage.setItem("buttonState", "on");
    resetButton.style.marginLeft = "0"; // Adjust the margin when ON/Off button text changes
  }
}

function sendFrameValues(frameValues) {
  if (socket.readyState === WebSocket.OPEN) {
    socket.send(
      JSON.stringify({
        type: "frameValues",
        values: frameValues,
      })
    );
  }
}

function sendProgramStartedMessage() {
  if (socket.readyState === WebSocket.OPEN) {
    socket.send(
      JSON.stringify({
        type: "start",
      })
    );
  }
}

function startProgram() {
  const startMessage = document.getElementById("startMessage");
  startMessage.innerText = "Program has started";
  startMessage.style.display = "block";

  const trueArray = ["start"];
  console.log("Value:", trueArray);

  // Send the trueArray message to the server
  socket.send(
    JSON.stringify({
      type: "start",
      message: trueArray,
    })
  );
}

function setButtonState() {
  const toggleButton = document.getElementById("toggleButton");
  const additionalButtonsDiv = document.getElementById("additionalButtons");
  const buttonState = localStorage.getItem("buttonState");

  if (buttonState === "off") {
    toggleButton.innerText = "Off";
    toggleButton.classList.remove("btn-primary");
    toggleButton.classList.add("btn-secondary");
    additionalButtonsDiv.style.display = "block";
  } else {
    toggleButton.innerText = "ON";
    toggleButton.classList.remove("btn-secondary");
    toggleButton.classList.add("btn-primary");
    additionalButtonsDiv.style.display = "none";
  }
}

function showAlert(message) {
  const alertDiv = document.createElement("div");
  alertDiv.classList.add("alert", "alert-success");
  alertDiv.innerHTML = `
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        ${message}
    `;

  document.body.appendChild(alertDiv);

  setTimeout(() => {
    alertDiv.remove();
  }, 5000);
}

function submitFrames() {
  const frameAValue = parseInt(document.getElementById("frameA").value) || 0;
  const frameBValue = parseInt(document.getElementById("frameB").value) || 0;
  const frameCValue = parseInt(document.getElementById("frameC").value) || 0;

  const frameValues = [frameAValue, frameBValue, frameCValue];
  console.log("Frame values:", frameValues);

  document.getElementById(
    "frameAInfo"
  ).innerText = `Frame A input: ${frameAValue}`;
  document.getElementById(
    "frameBInfo"
  ).innerText = `Frame B input: ${frameBValue}`;
  document.getElementById(
    "frameCInfo"
  ).innerText = `Frame C input: ${frameCValue}`;

  const additionalButtonsDiv = document.getElementById("additionalButtons");
  const infoDiv = document.getElementById("info");
  const startButton = document.getElementById("startButton");
  const resetButton = document.getElementById("resetButton");

  additionalButtonsDiv.style.display = "none";
  infoDiv.style.display = "block";
  startButton.style.display = "block";
  document.getElementById("toggleButton").style.display = "none"; // Hide "Off" button
  resetButton.style.display = "block"; // Show "Reset" button

  // Send frameValues array to the server
  socket.send(JSON.stringify(frameValues));
}

function resetFrames() {
  // Reset frame inputs
  document.getElementById("frameA").value = "";
  document.getElementById("frameB").value = "";
  document.getElementById("frameC").value = "";

  // Reset frame info display
  document.getElementById("frameAInfo").innerText = "";
  document.getElementById("frameBInfo").innerText = "";
  document.getElementById("frameCInfo").innerText = "";

  // Hide the reset button
  document.getElementById("resetButton").style.display = "none";

  // Display the input section again
  const toggleButton = document.getElementById("toggleButton");
  toggleButton.innerText = "OFF"; // Set the button text to "Off"
  toggleButton.classList.remove("btn-primary");
  toggleButton.classList.add("btn-secondary");
  document.getElementById("additionalButtons").style.display = "block";
  document.getElementById("info").style.display = "none";

  // Show the "Off" button
  toggleButton.style.display = "block";
}

setButtonState();

connectWebSocket();
