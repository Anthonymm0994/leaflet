#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🌿 Leaflet Arrow Explorer - Test Suite');
console.log('=====================================\n');

// Colors for output
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m',
  bold: '\x1b[1m'
};

// Test results
const results = {
  unit: { passed: 0, failed: 0, total: 0 },
  integration: { passed: 0, failed: 0, total: 0 },
  e2e: { passed: 0, failed: 0, total: 0 }
};

// Helper function to run tests
function runTestSuite(suiteName, testPath) {
  console.log(`${colors.blue}${colors.bold}Running ${suiteName} tests...${colors.reset}`);
  
  try {
    const output = execSync(`npx jest ${testPath} --verbose --no-coverage`, { 
      encoding: 'utf8',
      stdio: 'pipe'
    });
    
    // Parse test results
    const lines = output.split('\n');
    let passed = 0;
    let failed = 0;
    let total = 0;
    
    for (const line of lines) {
      if (line.includes('PASS')) {
        passed++;
        total++;
      } else if (line.includes('FAIL')) {
        failed++;
        total++;
      }
    }
    
    results[suiteName.toLowerCase()] = { passed, failed, total };
    
    console.log(`${colors.green}✅ ${suiteName} tests completed: ${passed} passed, ${failed} failed${colors.reset}\n`);
    return true;
    
  } catch (error) {
    console.log(`${colors.red}❌ ${suiteName} tests failed: ${error.message}${colors.reset}\n`);
    return false;
  }
}

// Main test execution
async function runAllTests() {
  console.log('Starting comprehensive test suite...\n');
  
  // Check if test files exist
  const testFiles = [
    { name: 'Unit', path: 'test/unit' },
    { name: 'Integration', path: 'test/integration' },
    { name: 'E2E', path: 'test/e2e' }
  ];
  
  let allPassed = true;
  
  for (const testFile of testFiles) {
    if (fs.existsSync(testFile.path)) {
      const success = runTestSuite(testFile.name, testFile.path);
      if (!success) {
        allPassed = false;
      }
    } else {
      console.log(`${colors.yellow}⚠️  ${testFile.name} tests not found at ${testFile.path}${colors.reset}\n`);
    }
  }
  
  // Summary
  console.log('📊 Test Summary');
  console.log('===============');
  
  let totalPassed = 0;
  let totalFailed = 0;
  let totalTests = 0;
  
  for (const [suite, result] of Object.entries(results)) {
    if (result.total > 0) {
      console.log(`${suite.charAt(0).toUpperCase() + suite.slice(1)}: ${result.passed}/${result.total} passed`);
      totalPassed += result.passed;
      totalFailed += result.failed;
      totalTests += result.total;
    }
  }
  
  console.log(`\nTotal: ${totalPassed}/${totalTests} tests passed`);
  
  if (allPassed && totalFailed === 0) {
    console.log(`\n${colors.green}${colors.bold}🎉 All tests passed!${colors.reset}`);
    process.exit(0);
  } else {
    console.log(`\n${colors.red}${colors.bold}❌ Some tests failed${colors.reset}`);
    process.exit(1);
  }
}

// Run tests
runAllTests().catch(error => {
  console.error(`${colors.red}Test runner error: ${error.message}${colors.reset}`);
  process.exit(1);
}); 