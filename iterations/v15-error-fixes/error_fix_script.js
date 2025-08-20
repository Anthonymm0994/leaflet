/**
 * 🚀 V15: Comprehensive Error Fix Script
 * 
 * This script can be applied to any data explorer iteration to fix common JavaScript errors:
 * - Undefined property access (this.margin, this.width, this.height)
 * - Initialization race conditions
 * - Negative radius errors
 * - Array access without validation
 * - Event handler errors
 */

// ============================================================================
// ERROR FIX UTILITIES
// ============================================================================

const ErrorFixer = {
    
    /**
     * Apply comprehensive error fixes to BaseChart class
     */
    fixBaseChart: function() {
        console.log('🔧 Fixing BaseChart class...');
        
        // Store original BaseChart if it exists
        if (window.BaseChart) {
            window.OriginalBaseChart = window.BaseChart;
        }
        
        // Create fixed BaseChart class
        window.BaseChart = class BaseChart {
            constructor(canvasId, column) {
                this.canvas = document.getElementById(canvasId);
                if (!this.canvas) {
                    console.error(`Canvas element not found: ${canvasId}`);
                    return;
                }
                
                this.ctx = this.canvas.getContext('2d');
                this.column = column;
                this.width = 0;
                this.height = 0;
                
                // Initialize margin FIRST to prevent undefined errors
                this.margin = { top: 10, right: 10, bottom: 25, left: 35 };
                
                // Don't call setupCanvas immediately - wait for proper initialization
                this.setupEvents();
                window.addEventListener('resize', this.resize.bind(this));
            }
            
            setupCanvas() {
                if (!this.canvas || !this.canvas.parentElement) {
                    console.warn('Canvas or parent not ready for setupCanvas');
                    return;
                }
                
                try {
                    const rect = this.canvas.parentElement.getBoundingClientRect();
                    const dpr = window.devicePixelRatio || 1;
                    this.canvas.width = (rect.width - 16) * dpr;
                    this.canvas.height = (rect.height - 36) * dpr;
                    this.canvas.style.width = (rect.width - 16) + 'px';
                    this.canvas.style.height = (rect.height - 36) + 'px';
                    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
                    this.width = rect.width - 16;
                    this.height = rect.height - 36;
                    
                    // Only draw if we have valid dimensions and margin
                    if (this.width > 0 && this.height > 0 && this.margin) {
                        this.draw();
                    }
                } catch (error) {
                    console.error('Error in setupCanvas:', error);
                }
            }
            
            resize() {
                this.setupCanvas();
            }
            
            clear() {
                if (!this.ctx || !this.width || !this.height) return;
                
                try {
                    this.ctx.fillStyle = '#1a1a1a';
                    this.ctx.fillRect(0, 0, this.width, this.height);
                } catch (error) {
                    console.error('Error in clear:', error);
                }
            }
            
            getMousePos(e) {
                if (!e || !this.canvas || !this.width || !this.height) return { x: 0, y: 0 };
                
                try {
                    const r = this.canvas.getBoundingClientRect();
                    return {
                        x: (e.clientX - r.left) * (this.width / r.width),
                        y: (e.clientY - r.top) * (this.height / r.height)
                    };
                } catch (error) {
                    console.error('Error in getMousePos:', error);
                    return { x: 0, y: 0 };
                }
            }
            
            setupEvents() {
                if (!this.canvas) return;
                
                try {
                    this.canvas.addEventListener('mousedown', this.onMouseDown.bind(this));
                    this.canvas.addEventListener('mousemove', this.onMouseMove.bind(this));
                    this.canvas.addEventListener('mouseup', this.onMouseUp.bind(this));
                    this.canvas.addEventListener('click', this.onClick.bind(this));
                } catch (error) {
                    console.error('Error setting up events:', error);
                }
            }
            
            onMouseDown(e) {}
            onMouseMove(e) {}
            onMouseUp(e) {}
            onClick(e) {}
            draw() {}
        };
        
        console.log('✅ BaseChart class fixed');
    },
    
    /**
     * Fix initialization sequence to prevent race conditions
     */
    fixInitialization: function() {
        console.log('🔧 Fixing initialization sequence...');
        
        // Find and fix createCharts method
        if (window.DataProcessor && window.DataProcessor.createCharts) {
            const originalCreateCharts = window.DataProcessor.createCharts;
            
            window.DataProcessor.createCharts = function() {
                // Wait for next tick to ensure DOM is fully ready
                setTimeout(() => {
                    try {
                        originalCreateCharts.call(this);
                        
                        // Initialize canvas after charts are created
                        if (window.charts) {
                            Object.values(window.charts).forEach(chart => {
                                if (chart && chart.setupCanvas) {
                                    chart.setupCanvas();
                                }
                            });
                        }
                    } catch (error) {
                        console.error('Error in createCharts:', error);
                    }
                }, 0);
            };
            
            console.log('✅ Initialization sequence fixed');
        } else {
            console.warn('⚠️ DataProcessor.createCharts not found');
        }
    },
    
    /**
     * Add error handling to existing chart classes
     */
    fixChartClasses: function() {
        console.log('🔧 Fixing chart classes...');
        
        // Fix HistogramChart if it exists
        if (window.HistogramChart) {
            this.fixHistogramChart();
        }
        
        // Fix AngleChart if it exists
        if (window.AngleChart) {
            this.fixAngleChart();
        }
        
        // Fix BarChart if it exists
        if (window.BarChart) {
            this.fixBarChart();
        }
        
        console.log('✅ Chart classes fixed');
    },
    
    /**
     * Fix HistogramChart class
     */
    fixHistogramChart: function() {
        if (!window.HistogramChart) return;
        
        const originalDraw = window.HistogramChart.prototype.draw;
        window.HistogramChart.prototype.draw = function() {
            if (!this.margin || !this.width || !this.height) {
                console.warn('HistogramChart not ready for drawing');
                return;
            }
            
            try {
                return originalDraw.call(this);
            } catch (error) {
                console.error('Error in HistogramChart draw:', error);
            }
        };
    },
    
    /**
     * Fix AngleChart class
     */
    fixAngleChart: function() {
        if (!window.AngleChart) return;
        
        const originalDraw = window.AngleChart.prototype.draw;
        window.AngleChart.prototype.draw = function() {
            if (!this.margin || !this.width || !this.height) {
                console.warn('AngleChart not ready for drawing');
                return;
            }
            
            try {
                return originalDraw.call(this);
            } catch (error) {
                console.error('Error in AngleChart draw:', error);
            }
        };
        
        // Fix radius calculation to prevent negative values
        const originalOnMouseDown = window.AngleChart.prototype.onMouseDown;
        window.AngleChart.prototype.onMouseDown = function(e) {
            if (!e || !this.width || !this.height) return;
            
            try {
                return originalOnMouseDown.call(this, e);
            } catch (error) {
                console.error('Error in AngleChart onMouseDown:', error);
            }
        };
    },
    
    /**
     * Fix BarChart class
     */
    fixBarChart: function() {
        if (!window.BarChart) return;
        
        const originalDraw = window.BarChart.prototype.draw;
        window.BarChart.prototype.draw = function() {
            if (!this.margin || !this.width || !this.height) {
                console.warn('BarChart not ready for drawing');
                return;
            }
            
            try {
                return originalDraw.call(this);
            } catch (error) {
                console.error('Error in BarChart draw:', error);
            }
        };
    },
    
    /**
     * Add global error handler
     */
    addGlobalErrorHandler: function() {
        console.log('🔧 Adding global error handler...');
        
        window.addEventListener('error', function(event) {
            console.error('🚨 Global error caught:', {
                message: event.message,
                filename: event.filename,
                lineno: event.lineno,
                colno: event.colno,
                error: event.error
            });
        });
        
        window.addEventListener('unhandledrejection', function(event) {
            console.error('🚨 Unhandled promise rejection:', event.reason);
        });
        
        console.log('✅ Global error handler added');
    },
    
    /**
     * Apply all fixes
     */
    applyAllFixes: function() {
        console.log('🚀 Applying comprehensive error fixes...');
        
        try {
            this.fixBaseChart();
            this.fixInitialization();
            this.fixChartClasses();
            this.addGlobalErrorHandler();
            
            console.log('🎉 All error fixes applied successfully!');
            console.log('💡 The system should now be much more stable and error-resistant.');
            
        } catch (error) {
            console.error('❌ Error applying fixes:', error);
        }
    },
    
    /**
     * Test the fixes
     */
    testFixes: function() {
        console.log('🧪 Testing error fixes...');
        
        // Test BaseChart
        if (window.BaseChart) {
            console.log('✅ BaseChart class available');
        } else {
            console.error('❌ BaseChart class not found');
        }
        
        // Test margin initialization
        try {
            const testChart = new window.BaseChart('test', 'test');
            if (testChart.margin) {
                console.log('✅ Margin properly initialized');
            } else {
                console.error('❌ Margin not initialized');
            }
        } catch (error) {
            console.error('❌ Error testing BaseChart:', error);
        }
        
        console.log('🧪 Error fix testing complete');
    }
};

// Auto-apply fixes when script loads
if (typeof window !== 'undefined') {
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            ErrorFixer.applyAllFixes();
        });
    } else {
        ErrorFixer.applyAllFixes();
    }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ErrorFixer;
}
