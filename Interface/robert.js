const fetch = require('node-fetch');

const serverAddress = 'http://192.168.0.1:29999'; // Replace with the server's address
const command = 'power off'; // Replace with your desired command

fetch(serverAddress, {
  method: 'POST',
  body: command,
  headers: {
    'Content-Type': 'text/plain',
  },
})
  .then((response) => response.text())
  .then((data) => {
    console.log('Received response from the server:', data);
  })
  .catch((error) => {
    console.error('Error:', error);
  });
