const { spawn } = require('child_process');
const path = require('path');

console.log('====================================================');
console.log('🚀  BHARAT NYAYA AI - FULL-STACK SYSTEM LAUNCHER');
console.log('====================================================');

const isWindows = process.platform === 'win32';
const npmCmd = isWindows ? 'npm.cmd' : 'npm';
const npxCmd = isWindows ? 'npx.cmd' : 'npx';

// 1. Launch Backend
console.log('📡 Starting Backend Core API Server on http://localhost:5000 ...');
const backend = spawn('node', ['src/server.js'], {
  cwd: path.resolve(__dirname, 'backend'),
  stdio: 'inherit',
  shell: true,
});

// 2. Launch Frontend
console.log('💻 Starting Frontend Web Application on http://localhost:5173 ...');
const frontend = spawn(npmCmd, ['run', 'dev'], {
  cwd: path.resolve(__dirname, 'frontend'),
  stdio: 'inherit',
  shell: true,
});

function cleanup() {
  console.log('\n🛑 Stopping Bharat Nyaya AI services...');
  try { backend.kill('SIGINT'); } catch (e) {}
  try { frontend.kill('SIGINT'); } catch (e) {}
  process.exit(0);
}

process.on('SIGINT', cleanup);
process.on('SIGTERM', cleanup);
