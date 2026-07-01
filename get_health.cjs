const http = require('http');
http.get('http://localhost:3000/_stcore/health', (res) => {
  console.log('Status Code:', res.statusCode);
  console.log('Headers:', res.headers);
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => console.log('Body:', data));
});
