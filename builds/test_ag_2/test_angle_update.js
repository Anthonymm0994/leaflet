// Test script to verify angle chart updates
// Run this in the browser console after opening real_next_best_yet.html

console.log('Testing angle chart updates...');

// Check if charts object exists
console.log('Charts object:', charts);
console.log('Angle chart:', charts.angle);

// Check current filter state
console.log('Current filters:', filters);

// Test applying a filter
console.log('\nApplying width filter...');
filters.width = [30, 70];
applyFilters();

// Wait a bit and check if angle chart was redrawn
setTimeout(() => {
    console.log('Filter applied. Check if angle chart updated visually.');
    console.log('Clearing filter...');
    filters.width = null;
    applyFilters();
}, 1000);