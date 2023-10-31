const http = require('http');
const WebSocket = require('ws');

const server = http.createServer();
const wss = new WebSocket.Server({ noServer: true });

wss.on('connection', (socket, request) => {
  const clientAddress = request.connection.remoteAddress;
  console.log(`Client connected from IP: ${clientAddress}`);

  // Menangani pesan dari client
  socket.on('message', (message) => {
    console.log(`Received from client at IP ${clientAddress}: ${message}`);
    // Mengirim balasan ke client
    socket.send(`Server: You said: ${message}`);    
  });
});

server.on('upgrade', (request, socket, head) => {
  wss.handleUpgrade(request, socket, head, (socket) => {
    wss.emit('connection', socket, request);
  });
});

const PORT = 8080;
const HOST = '127.0.0.1';

server.listen(PORT, HOST, () => {
  console.log(`Server listening on ${HOST}:${PORT}`);
});
