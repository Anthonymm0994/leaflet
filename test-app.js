const { spawn } = require('child_process');
const path = require('path');

console.log('🧪 Testing Leaflet Arrow Explorer...');

// Start the application
const app = spawn('npm', ['start'], {
  stdio: ['pipe', 'pipe', 'pipe'],
  shell: true
});

let output = '';
let errorOutput = '';

app.stdout.on('data', (data) => {
  output += data.toString();
  console.log('📤 STDOUT:', data.toString());
});

app.stderr.on('data', (data) => {
  errorOutput += data.toString();
  console.log('❌ STDERR:', data.toString());
});

app.on('close', (code) => {
  console.log(`\n🏁 Application exited with code ${code}`);
  
  if (code === 0) {
    console.log('✅ Application started successfully!');
  } else {
    console.log('❌ Application failed to start');
    console.log('Error output:', errorOutput);
  }
  
  // Kill the process after 10 seconds
  setTimeout(() => {
    app.kill();
    process.exit(0);
  }, 10000);
});

// Handle process termination
process.on('SIGINT', () => {
  console.log('\n🛑 Stopping test...');
  app.kill();
  process.exit(0);
});

console.log('⏳ Application starting... (will auto-stop in 10 seconds)'); 