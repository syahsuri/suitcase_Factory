let websocket;
const address = "localhost";
const portDirect = 1080;
const portServer = 8080;

document
  .getElementById("continueButton")
  .addEventListener("click", function (event) {
    event.preventDefault();
    continueButton();
  });


  function autoConnect() {
    setTimeout(() => {
      const websocket = new WebSocket(`ws://${address}:${portDirect}`);
      const message = "play\r\n";
  
      websocket.addEventListener("open", () => {
        console.log("WebSocket connected");
        websocket.send(message);
        websocket.send("brake release\r\n");
      });
  
      websocket.addEventListener("message", (event) => {
        console.log("Received from server.js:", event.data);
        // Process the received data from server.js as needed
      });
  
      websocket.addEventListener("close", () => {
        console.log("WebSocket connection closed");
      });
    }, 3000); // 3-second delay (3000 milliseconds)
  }
  
function startUp() {
  const websocket = new WebSocket(`ws://${address}:${portDirect}`);
  const message = "power on\r\n";

  websocket.addEventListener("open", () => {
    console.log("WebSocket connected");
    websocket.send(message);
    websocket.send("brake release\r\n");
  });

  websocket.addEventListener("message", (event) => {
    console.log("Received from server.js:", event.data);
    // Process the received data from server.js as needed
  });

  websocket.addEventListener("close", () => {
    console.log("WebSocket connection closed");
  });

  // Update status
  status();
  setInterval(status, 5000);
}

function sendRobotStats() {
  // Create a single WebSocket connection
  const websocket = new WebSocket(`ws://${address}:${portDirect}`);

  websocket.addEventListener("message", (event) => {
      console.log("Received from server.js:", event.data);
      // Process the received data from server.js as needed
  });

  websocket.addEventListener("close", () => {
      console.log("WebSocket connection closed");
  });

  // Update status
  statusRobot();
  setInterval(statusRobot, 5000);
}

// Function to establish WebSocket connection
function connectWebSocket() {
  const socketUrl = `ws://${address}:${portServer}`;

  websocket = new WebSocket(socketUrl);
  const sendId = "3";
  websocket.addEventListener("open", () => {
    console.log("WebSocket connected");
    websocket.send(sendId);
  });
}

function continueButton() {
  send_command("ready", 1).then(() => {
    window.location.href = "insertframe.html";
  });
}

async function inspectButton() {
  send_command("inspect", 1);

  Swal.fire({
    title: "Warning!",
    text: "The robot is moving, please standby.",
    icon: "warning",
    showConfirmButton: false,
    allowOutsideClick: false,
    willOpen: () => {
      Swal.showLoading();
    },
    didClose: () => {},
    showCancelButton: false,
  });

  await delay(5000);

  Swal.fire({
    title: "Inspection",
    text: "You are now able to inspect, repair or change the tools.",
    icon: "info",
    showConfirmButton: true,
    confirmButtonText: "Dispose glue",
    allowOutsideClick: false,
    cancelButtonText: "Done",
    showCancelButton: true,
  }).then((result) => {
    if (result.isConfirmed) {
      send_command("dispose", 1);

      Swal.fire({
        title: "Warning!",
        text: "The robot is disposing glue, please standby.",
        icon: "warning",
        showConfirmButton: false,
        allowOutsideClick: false,
        willOpen: () => {
          Swal.showLoading();
        },
        didClose: () => {},
        showCancelButton: false,
      });

      setTimeout(() => {
        Swal.fire({
          title: "Caution",
          text: "Clean the nozzle if necessary.",
          icon: "warning",
          confirmButtonText: "Continue",
          allowOutsideClick: false,
          showCancelButton: false,
          didClose: () => {
            finish();
          },
        });
      }, 5000);
    } else {
      console.log("Test");
      finish();
    }
  });

  function finish() {
    send_command("back", 1);

    Swal.fire({
      title: "Warning!",
      text: "The robot is moving, please standby.",
      icon: "warning",
      showConfirmButton: false,
      allowOutsideClick: false,
      willOpen: () => {
        Swal.showLoading();
      },
      didClose: () => {},
      showCancelButton: false,
    });

    setTimeout(() => {
      Swal.close();
    }, 5000);
  }
}

function exitButton() {
  Swal.fire({
    title: "Shutdown robot",
    icon: "info", // Use 'error' icon for a red alert
    confirmButtonText: "Ok", // Change the text of the confirmation button
    allowOutsideClick: false,
    willOpen: () => {
      Swal.showLoading();
    },
    didClose: () => {},
  }).then((result) => {
    if (result.isConfirmed) {
      // The user clicked "OK", do something if needed
    }
  });

  send_command("stop", 1);
}

function disposeButton() {
  Swal.fire({
    title: "Warning! Robot is moving!",
    icon: "warning", // Use 'error' icon for a red alert
    confirmButtonText: "Continue", // Change the text of the confirmation button
    allowOutsideClick: false,
    willOpen: () => {
      Swal.showLoading();
    },
    didClose: () => {},
  }).then((result) => {
    if (result.isConfirmed) {
      // The user clicked "OK", do something if needed
    }
  });

  send_command("dispose", 1);
}

const socket = new WebSocket(`ws://${address}:${portServer}`); // Replace with your server's WebSocket URL
const element = document.getElementById("statusServer");

socket.addEventListener("open", (event) => {
  log("Connected to the server");
  element.innerHTML = ` <div class="mb-0"><b>Server:</b></div></br> <i class="fa-solid fa-square-check fa-2xl"style="color: green;"></i><div>`;
});

socket.addEventListener("message", (event) => {
  //if(!event.data.startsWith("!"))
  //{
  log("Server: " + event.data);
  //}
});

socket.addEventListener("close", (event) => {
  log("Disconnected from the server\n");
  element.innerHTML = `<b>Server:</b> </br><i class="fa-solid fa-plug-circle-xmark fa-2xl" style="color: #ff0000;"></i>`;
});

socket.addEventListener("error", (event) => {
  log("WebSocket error");
});

function status() {
  send_command("status", 1);
  send_command("status", 2);
}
// Array to store responses
// Object to store responses with associated commands
const responses = {};

function statusRobot() {
  robot_command("programState");
  robot_command("robotmode");
  robot_command("safetystatus");
}

function robot_command(command) {
  const websocket = new WebSocket(`ws://${address}:${portDirect}`);
  const message = `${command}\r\n`;

  websocket.addEventListener("open", () => {
      console.log("WebSocket connected");
      websocket.send(message);
  });

  websocket.addEventListener("message", (event) => {
      console.log("Received from server.js2:", event.data);
      
      // Display the received data in the respective resultDiv
      if(!event.data.includes(":"))
      {
        updateStatusDisplay("programState", event.data);
        return;
      }
      const part = event.data.split(":");
      const divId = part[0].trim();
      const status = part[1].trim();
      updateStatusDisplay(divId, status);
  });

  websocket.addEventListener("close", () => {
      console.log("WebSocket connection closed");
  });
}

function updateStatusDisplay(divId, data) {
  // Select the HTML div where you want to display the status
  const resultDiv = document.getElementById(divId);

  // Update the content of the selected div
  resultDiv.innerHTML = divId + ": " + data;
}

// Call statusRobot when the page loads
document.addEventListener("DOMContentLoaded", () => {
  statusRobot();
});


// Call statusRobot when the page loads
document.addEventListener("DOMContentLoaded", () => {
  statusRobot();
});

const socketDirect = new WebSocket(`ws://${address}:${portDirect}`); // Replace with your server's WebSocket URL

function handle_direct_commands() {}

function send_command(command, client = -1) {
  return new Promise((resolve, reject) => {
    // Establish a WebSocket connection to the server.js
    const websocket = new WebSocket(`ws://${address}:${portServer}`);

    let data = `[${client}]` + command;
    if (client < 0) {
      data = command;
    }

    websocket.addEventListener("open", () => {
      websocket.send(data);
      resolve();
    });

    websocket.addEventListener("message", (event) => {
      receive_command(event.data);
    });
  });
}

function receive_command(command) {
  handle_commands(command);
}

function handle_commands(command) {
  if (command.startsWith("status")) {
    const startIdx = command.indexOf("(");
    const endIdx = command.indexOf(")");

    if (startIdx !== -1 && endIdx !== -1) {
      const i = command.slice(startIdx + 1, endIdx);

      const statusStr = command.split(":")[1].trim();
      const status = statusStr === "true";

      if (i == 1) {
        const element = document.getElementById("statusRobot");
        if (status) {
          element.innerHTML = `<div class="mb-0"><b>UR10:</b></div></br> <i class="fa-solid fa-square-check fa-2xl "style="color: green;"></i>`;
        } else {
          element.innerHTML = `<div class="mb-0"><b>UR10:</b></div></br> <i class="fa-solid fa-plug-circle-xmark fa-2xl" style="color: #ff0000;"></i>`;
        }
      }

      if (i == 2) {
        const element = document.getElementById("statusCamera");
        if (status) {
          element.innerHTML = `<div class="mb-0"><b>Camera:</b></div> </br><i class="fa-solid fa-square-check fa-2xl bg-success"style="color: green;"></i>`;
        } else {
          element.innerHTML = `<div class="mb-0"><b>Camera:</b></div></br> <i class="fa-solid fa-plug-circle-xmark fa-2xl" style="color: #ff0000;"></i>`;
        }
      }
    }
  }
}

const messageLog = document.getElementById("messageLog");
function log(log, timestamp = true) {
  const time = new Date().toLocaleTimeString();
  if (time) {
    messageLog.textContent += `[${time}] ${log}\n`;
    return;
  }
  messageLog.textContent += `${log}\n`;
}

async function delay(milliseconds) {
  return new Promise((resolve) => {
    setTimeout(resolve, milliseconds);
  });
}

// Connect to WebSocket when the page loads
connectWebSocket();
startUp();
autoConnect();
sendRobotStats();
