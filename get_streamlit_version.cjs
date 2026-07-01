const { execSync } = require('child_process');
console.log(execSync('pip show streamlit').toString());
