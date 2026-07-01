const WebSocket = require('ws');
const ws = new WebSocket('ws://localhost:3000/_stcore/stream');
ws.on('open', function open() {
  console.log('connected');
  ws.send('ping');
});
ws.on('message', function incoming(data) {
  console.log('message: %s', data);
});
ws.on('error', function error(err) {
  console.log('error: ', err);
});
