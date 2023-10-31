const net = require('net');

let name_socket = "server";
let server_socket = null;

// Connect to server
// Returns true or false whether the connection has been made (attempts = 0 for no limit)
async function connect_to_server(attempts = 0) {
    if (is_connected_to_server()) {
        return true;
    }

    let id = "3";
    let port = 10000;
    let ip = "127.0.0.1";
    let attempt = 0;

    console.log("Attempting to connect...");
    while (attempt < attempts || attempts === 0) {
      
        if (server_socket != null && server_socket.writable) {
            send_command(id);
            console.log("Connected to server");
            return true;
        }

        server_socket = new net.Socket();
        try {
            await new Promise((resolve, reject) => {
                server_socket.connect(port, ip, () => {
                    resolve();
                });
                server_socket.on('error', (err) => {
                    reject(err);
                });
            });
        } catch (err) {
            // ConnectionRefusedError handling
        }
        attempt++;
        await sleep(1000);
    }
    return false;
}

// Returns true or false whether it's connected to the server
function is_connected_to_server() {
    return (server_socket != null && server_socket.writable);
}

// Wait for command
// Returns false if not receiving command after timeout (timeout = 0 for no limit)
async function wait_for_command(timeout = 0) {
    if (server_socket) {
        if (timeout === 0) {
            return new Promise((resolve) => {
                server_socket.once('data', (data) => {
                    resolve(data.toString());
                });
            });
        } else {
            server_socket.setTimeout(timeout);
            return new Promise((resolve) => {
                server_socket.once('data', (data) => {
                    resolve(data.toString());
                });
                server_socket.once('timeout', () => {
                    resolve(false);
                });
            });
        }
    } else {
        return false;
    }
}

// Send command to server
// Returns true or false whether it sent the command. Retry = true will continue trying.
function send_command(command, retry = false) {
    console.log("Cmd:" + command);
    if (server_socket) {
        try {
            server_socket.write(command);
            return true;
        } catch (err) {
            server_socket = null;
        }
    }
    if (retry) {
        setTimeout(() => {
            send_command(command, true);
        }, 1000);
    }
    return false;
}

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function start() {
    await connect_to_server();
}

async function main() {
    await connect_to_server();

    // Continue running to listen for commands
    while (true) {
        //const command = await wait_for_command();
        //if (command !== false) {
        //    console.log("Received command: " + command);
        //    // Process the received command here
        //}
    }
}

main(); // Start the script and keep it running