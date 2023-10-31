const address = "localhost";
const portDirect = 1080;
const portServer = 8080;


function showModal() {
  Swal.fire({
    title: "Task completed",
    icon: "success",
    confirmButtonText: "Ok",
  });
}

function connectWebSocket() {
  // Replace with your WebSocket server URL
  const socketUrl = "ws://localhost:8080";

  websocket = new WebSocket(socketUrl);

  websocket.onopen = () => {
    console.log("WebSocket connection established.");
  };

  websocket.onclose = () => {
    console.log("WebSocket connection closed.");
  };

  websocket.onerror = (error) => {
    console.error("WebSocket error:", error);
  };
}

connectWebSocket();



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
  resultDiv.innerHTML = `<b> ${divId} </b>` + ": " +"</br>" + data;
}

// Call statusRobot when the page loads
document.addEventListener("DOMContentLoaded", () => {
  statusRobot();
});

function toggleFrameInput(checkbox) {
  const frameInput = document.getElementById("frameInput");
  const statusElement = document.getElementById("statusRobot");

  // Display or hide the frameInput based on the checkbox state
  frameInput.style.display = checkbox.checked ? "block" : "none";

  // Establish a WebSocket connection
  const websocket = new WebSocket("ws://localhost:1080");

  // Define the message to send
 
  websocket.addEventListener("message", (event) => {
    const receivedData = event.data;
    console.log("Received from server.js:", receivedData);

    // Update the status element with the received data
    // statusElement.innerHTML = `Robot Status: ${receivedData}`;
  });

  websocket.addEventListener("close", () => {
    console.log("WebSocket connection closed");
  });
}

function goBack() {
  back()
  // Add your code to handle the "back" button functionality here  
}

const radioButtons = document.querySelectorAll('input[name="inlineRadioOptions"]');



let messageCount = 0; // Variable to keep track of the message count
let totalFrameValue = 0;
let startMsg = "";

radioButtons.forEach(radioButton => {
  radioButton.addEventListener("change", (event) => {
    // Update startMsg with the selected option's value
    startMsg = event.target.value;
  });
});

function submitFrames() {
  const frameA = document.getElementById("frameA").value || 0;
  const frameB = document.getElementById("frameB").value || 0;
  const frameC = document.getElementById("frameC").value || 0;

  totalFrameValue = parseInt(frameA)+parseInt(frameB)+parseInt(frameC)
  console.log(totalFrameValue);

  const progressBar = document.getElementById("messageProgressBar");
  progressBar.max = totalFrameValue;

  const infoDisplay = document.getElementById("infoDisplay");
  infoDisplay.innerHTML = `
  <div class="frames-container">
  <div class="frame-info" id="frameA">
    <p><b class="text-info">Closing frame:</b> ${frameA}</p>
  </div>

  <div class="frame-info" id="frameB">
    <p><b class="text-info">Corner frame:</b> ${frameB}</p>
  </div>

  <div class="frame-info" id="frameC">
    <p><b class="text-info">Double frame:</b> ${frameC}</p>
  </div>
</div>
`
  // const message = "[1]" + JSON.stringify(`(${frameA},${frameB},${frameC})`);
  const message = "[1]" + (`(${frameA},${frameB},${frameC})`);


  // Establish a WebSocket connection to the server.js
  const websocket = new WebSocket("ws://localhost:8080");

  websocket.addEventListener("open", () => {
    console.log("WebSocket connected");
    websocket.send(startMsg);
  
    // Add a delay of 1000 milliseconds (1 second) after sending the start message
    setTimeout(() => {
      websocket.send(message);
    }, 1500);
  });
  
  websocket.addEventListener("message", (event) => {
    console.log("Received from server.js:", event.data);
    // Process the received data from server.js as needed
  });

  websocket.addEventListener("close", () => {
    console.log("WebSocket connection closed");
  });

  document.getElementById("buttonContainer").style.display = "flex";
  document.getElementById("backButton").style.display = "none";
  document.getElementById("startBtn").style.display = "none";
 

}

function resetFrames() {
  // Reset frame values and clear info display
  document.getElementById("frameA").value = "";
  document.getElementById("frameB").value = "";
  document.getElementById("frameC").value = "";
  document.getElementById("infoDisplay").innerHTML = "";
  document.getElementById("buttonsDisplay").innerHTML = "";
}



function stopFrames() {
  console.log("STOP");

  // Establish a WebSocket connection to the server.js
  const websocket = new WebSocket("ws://localhost:1080");

  // Define the message to send
  const message = "power off\r\n"; // Replace with your desired message

  websocket.addEventListener("open", () => {
    console.log("WebSocket connected");
    // Send the message when the WebSocket is open
    websocket.send(message);
  });

  websocket.addEventListener("message", (event) => {
    console.log("Received from server.js:", event.data);
    // Process the received data from server.js as needed
  });

  websocket.addEventListener("close", () => {
    console.log("WebSocket connection closed");
  });
}

function pause() {
  console.log("PAUSING");
  // Establish a WebSocket connection to the server.js
  const websocket = new WebSocket("ws://localhost:1080");

  // Define the message to send
  const message = "pause\r\n"; // Replace with your desired message

  websocket.addEventListener("open", () => {
    console.log("WebSocket connected");
    // Send the message when the WebSocket is open
    websocket.send(message);
  });

  websocket.addEventListener("message", (event) => {
    console.log("Received from server.js:", event.data);
    // Process the received data from server.js as needed
  });

  websocket.addEventListener("close", () => {
    console.log("WebSocket connection closed");
  });

  // document.getElementById("playtBtn").style.display = "inline";
  // document.getElementById("pauseBtn").style.display = "none";

  
}

function play() {
  console.log("PLAY");

  // Establish a WebSocket connection to the server.js
  const websocket = new WebSocket("ws://localhost:1080");

  // Define the message to send
  const message = "play\r\n"; // Replace with your desired message
  
  

  websocket.addEventListener("open", () => {
    console.log("WebSocket connected");
    // Send the message when the WebSocket is open
    websocket.send(message);
  });

  websocket.addEventListener("message", (event) => {
    console.log("Received from server.js:", event.data);
    // Process the received data from server.js as needed
  });

  websocket.addEventListener("close", () => {
    console.log("WebSocket connection closed");
  });


  // document.getElementById("pauseBtn").style.display = "inline";
  // document.getElementById("playtBtn").style.display = "none";

}

function stop() {

  document.getElementById("frameA").value = "";
  document.getElementById("frameB").value = "";
  document.getElementById("frameC").value = "";
  document.getElementById("infoDisplay").innerHTML = "";
  document.getElementById("buttonsDisplay").innerHTML = "";
  // Establish a WebSocket connection to the server.js
  const websocket = new WebSocket("ws://localhost:1080");

  // Define the message to send
  const message = "stop\r\n"; // Replace with your desired message

  websocket.addEventListener("open", () => {
    console.log("WebSocket connected");
    // Send the message when the WebSocket is open
    websocket.send(message);
  });

  websocket.addEventListener("message", (event) => {
    console.log("Received from server.js:", event.data);
    // Process the received data from server.js as needed
  });

  websocket.addEventListener("close", () => {
    console.log("WebSocket connection closed");
  });

  document.getElementById("backButton").style.display = "inline";
  // document.getElementById("startBtn").style.display = "inline";
  // document.getElementById("playtBtn").style.display = "inline";
  // document.getElementById("pauseBtn").style.display = "none";


}

function stopGlueing() {

  const websocket = new WebSocket("ws://localhost:1080");

  // Define the message to send
  const message = "set_digital_out(1, True)"; // Replace with your desired message

  websocket.addEventListener("open", () => {
    console.log("WebSocket connected");
    // Send the message when the WebSocket is open
    websocket.send(message);
  });

  websocket.addEventListener("message", (event) => {
    console.log("Received from server.js:", event.data);
    // Process the received data from server.js as needed
  });

  websocket.addEventListener("close", () => {
    console.log("WebSocket connection closed");
  });

}

function validateNonNegativeInput(inputId) {
  const inputElement = document.getElementById(inputId);
  const value = inputElement.value;

  if (value < 0) {
    inputElement.value = 0; // Set the value to 0 if negative
  }

  

}
 // Variable to keep track of the message count

function updateInterface(data) {
  const textarea = document.getElementById("messageTextArea");
  textarea.value += `Received from Python server: ${data}\n`; // Append new message on a new line

  // Update the progress bar only when the message is "frame completed"
  if (data.trim() === "frame completed") {
    messageCount++;
    const progressBar = document.getElementById("messageProgressBar");
    progressBar.value = messageCount;
    console.log("a"+toggleFrameInput);
    if (messageCount >= totalFrameValue) {
      // Reset the message count and progress bar when it reaches totalFrameValue
      messageCount = 0;
      progressBar.value = 0;

      // Show the modal
      showModal();
    }
  }else if (data.trim() === "frames completed") {
    showModal();
  }
} 
  // Show the modal when "frames completed" is received


function showModal() {
  Swal.fire({
    title: "Task completed",
    icon: "success",
    confirmButtonText: "Ok",
  }).then((result) => {
    if (result.isConfirmed) {
      goBack();
    }
  });
}

// Make sure to connect to the WebSocket and set up the message event handling as needed
const socket = new WebSocket("ws://localhost:8080");

socket.addEventListener("message", (event) => {
  console.log("Received from server.js:", event.data);
  updateInterface(event.data);
});

function status() {
  const statusElement = document.getElementById("statusRobot");

  function updateStatus(data) {
    // Append the received data to the inner HTML of the status element
    statusElement.innerHTML += `Received from Python server: ${data}<br>`;
  }

  const websocket = new WebSocket("ws://localhost:1080");

  websocket.addEventListener("message", (event) => {
    const receivedData = event.data;
    updateStatus(receivedData);
  });
}

function back(){
  // Establish a WebSocket connection to the server.js
  const websocket = new WebSocket("ws://localhost:8080");

  // Define the message to send
  const message = "stop"; // Replace with your desired message

  websocket.addEventListener("open", () => {
    console.log("WebSocket connected");
    // Send the message when the WebSocket is open
    websocket.send(message);

    window.history.back();
  });

  websocket.addEventListener("message", (event) => {
    console.log("Received from server.js:", event.data);
    // Process the received data from server.js as needed
  });

  websocket.addEventListener("close", () => {
    console.log("WebSocket connection closed");
  });
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

