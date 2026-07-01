const { execSync } = require('child_process');
console.log(execSync('streamlit config show').toString());
