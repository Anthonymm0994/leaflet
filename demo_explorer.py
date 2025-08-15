#!/usr/bin/env python3
"""
Demo script for the Data Explorer

This script demonstrates various configurations and use cases
for the modular data explorer system.
"""

import json
from pathlib import Path
from data_loader import DataExplorerConfig

def demo_basic_usage():
    """Demonstrate basic usage with numerical data"""
    print("Demo 1: Basic Numerical Data Explorer")
    print("-" * 40)
    
    config = DataExplorerConfig()
    config.load_csv("test_data/test_data_numerical.csv")
    config.set_title("Employee Data Explorer")
    
    # Generate HTML
    config.generate_html("test_data/demo_basic_numerical.html")
    
    print(f"✓ Generated basic numerical explorer with {len(config.config['data'])} rows")
    print(f"  - Columns: {', '.join(config.config['columns'][:5])}...")
    print(f"  - Charts: {len(config.config['chartTypes'])} auto-generated charts")
    print(f"  - File: test_data/demo_basic_numerical.html")
    print()

def demo_custom_charts():
    """Demonstrate custom chart configuration"""
    print("Demo 2: Custom Chart Configuration")
    print("-" * 40)
    
    config = DataExplorerConfig()
    config.load_csv("test_data/test_data_mixed.csv")
    config.set_title("Custom Retail Analytics Dashboard")
    
    # Clear default charts and create custom ones
    config.set_chart_types([])
    
    # Add specific charts with custom titles
    config.add_chart({
        "type": "histogram",
        "column": "age",
        "title": "Customer Age Distribution"
    })
    
    config.add_chart({
        "type": "histogram", 
        "column": "income",
        "title": "Income Distribution"
    })
    
    config.add_chart({
        "type": "categorical",
        "column": "product_category",
        "title": "Product Category Sales"
    })
    
    config.add_chart({
        "type": "categorical",
        "column": "store_location",
        "title": "Store Performance by Location"
    })
    
    config.add_chart({
        "type": "categorical",
        "column": "customer_type",
        "title": "Customer Type Breakdown"
    })
    
    config.add_chart({
        "type": "histogram",
        "column": "purchase_amount",
        "title": "Purchase Amount Distribution"
    })
    
    # Generate HTML
    config.generate_html("test_data/demo_custom_charts.html")
    
    print(f"✓ Generated custom chart explorer with {len(config.config['data'])} rows")
    print(f"  - Custom charts: {len(config.config['chartTypes'])}")
    for chart in config.config['chartTypes']:
        print(f"    - {chart['title']} ({chart['type']})")
    print(f"  - File: test_data/demo_custom_charts.html")
    print()

def demo_time_series():
    """Demonstrate time-based data exploration"""
    print("Demo 3: Time Series Data Explorer")
    print("-" * 40)
    
    config = DataExplorerConfig()
    config.load_csv("test_data/test_data_time.csv")
    config.set_title("Time Series Analysis Dashboard")
    
    # Customize charts for time data
    config.set_chart_types([])
    
    config.add_chart({
        "type": "time",
        "column": "time",
        "title": "Visit Time Distribution"
    })
    
    config.add_chart({
        "type": "histogram",
        "column": "duration_minutes",
        "title": "Session Duration"
    })
    
    config.add_chart({
        "type": "categorical",
        "column": "category",
        "title": "Time of Day Categories"
    })
    
    config.add_chart({
        "type": "categorical",
        "column": "day_of_week",
        "title": "Weekly Pattern"
    })
    
    config.add_chart({
        "type": "categorical",
        "column": "month",
        "title": "Monthly Trends"
    })
    
    config.add_chart({
        "type": "histogram",
        "column": "wait_time",
        "title": "Wait Time Distribution"
    })
    
    # Generate HTML
    config.generate_html("test_data/demo_time_series.html")
    
    print(f"✓ Generated time series explorer with {len(config.config['data'])} rows")
    print(f"  - Time-based charts: {len(config.config['chartTypes'])}")
    for chart in config.config['chartTypes']:
        print(f"    - {chart['title']} ({chart['type']})")
    print(f"  - File: test_data/demo_time_series.html")
    print()

def demo_large_dataset():
    """Demonstrate handling of large datasets"""
    print("Demo 4: Large Dataset Performance Test")
    print("-" * 40)
    
    config = DataExplorerConfig()
    config.load_csv("test_data/test_data_large.csv")
    config.set_title("Large Dataset Performance Demo")
    
    # Generate HTML
    config.generate_html("test_data/demo_large_dataset.html")
    
    print(f"✓ Generated large dataset explorer with {len(config.config['data']):,} rows")
    print(f"  - Columns: {', '.join(config.config['columns'])}")
    print(f"  - Charts: {len(config.config['chartTypes'])} auto-generated")
    print(f"  - File: test_data/demo_large_dataset.html")
    print()

def demo_angle_data():
    """Demonstrate angular data visualization"""
    print("Demo 5: Angular Data Explorer")
    print("-" * 40)
    
    config = DataExplorerConfig()
    config.load_csv("test_data/test_data_angle.csv")
    config.set_title("Wind and Weather Analysis")
    
    # Customize for angular data
    config.set_chart_types([])
    
    config.add_chart({
        "type": "histogram",
        "column": "angle_degrees",
        "title": "Wind Direction Distribution"
    })
    
    config.add_chart({
        "type": "categorical",
        "column": "compass_direction",
        "title": "Compass Direction Breakdown"
    })
    
    config.add_chart({
        "type": "histogram",
        "column": "wind_speed",
        "title": "Wind Speed Distribution"
    })
    
    config.add_chart({
        "type": "histogram",
        "column": "temperature",
        "title": "Temperature Distribution"
    })
    
    config.add_chart({
        "type": "categorical",
        "column": "season",
        "title": "Seasonal Patterns"
    })
    
    config.add_chart({
        "type": "categorical",
        "column": "time_of_day",
        "title": "Time of Day Analysis"
    })
    
    # Generate HTML
    config.generate_html("test_data/demo_angle_data.html")
    
    print(f"✓ Generated angular data explorer with {len(config.config['data'])} rows")
    print(f"  - Angular charts: {len(config.config['chartTypes'])}")
    for chart in config.config['chartTypes']:
        print(f"    - {chart['title']} ({chart['type']})")
    print(f"  - File: test_data/demo_angle_data.html")
    print()

def demo_export_config():
    """Demonstrate configuration export and reuse"""
    print("Demo 6: Configuration Export and Reuse")
    print("-" * 40)
    
    # Create configuration
    config = DataExplorerConfig()
    config.load_csv("test_data/test_data_mixed.csv")
    config.set_title("Exportable Configuration Demo")
    
    # Customize charts
    config.set_chart_types([])
    config.add_chart({
        "type": "histogram",
        "column": "age",
        "title": "Age Distribution"
    })
    config.add_chart({
        "type": "categorical",
        "column": "product_category",
        "title": "Product Categories"
    })
    
    # Export configuration
    config.save_config("test_data/demo_config.json")
    
    # Generate HTML
    config.generate_html("test_data/demo_export_config.html")
    
    print(f"✓ Generated configuration export demo")
    print(f"  - Configuration saved to: test_data/demo_config.json")
    print(f"  - HTML generated to: test_data/demo_export_config.html")
    print(f"  - You can now reuse this configuration with other datasets")
    print()

def demo_advanced_features():
    """Demonstrate advanced features and customization"""
    print("Demo 7: Advanced Features Demo")
    print("-" * 40)
    
    config = DataExplorerConfig()
    config.load_csv("test_data/test_data_categorical.csv")
    config.set_title("Advanced Features Showcase")
    
    # Customize mini metrics
    config.set_mini_metrics([
        {"id": "filtered", "label": "Filtered Rows"},
        {"id": "percent", "label": "of Total"},
        {"id": "unique_countries", "label": "Unique Countries"},
        {"id": "unique_cities", "label": "Unique Cities"},
        {"id": "industry_breakdown", "label": "Industries"},
        {"id": "education_levels", "label": "Education Levels"}
    ])
    
    # Customize charts
    config.set_chart_types([])
    config.add_chart({
        "type": "categorical",
        "column": "country",
        "title": "Geographic Distribution"
    })
    config.add_chart({
        "type": "categorical",
        "column": "industry",
        "title": "Industry Breakdown"
    })
    config.add_chart({
        "type": "categorical",
        "column": "job_title",
        "title": "Job Title Distribution"
    })
    config.add_chart({
        "type": "categorical",
        "column": "education",
        "title": "Education Level Analysis"
    })
    config.add_chart({
        "type": "categorical",
        "column": "blood_type",
        "title": "Blood Type Distribution"
    })
    config.add_chart({
        "type": "categorical",
        "column": "favorite_color",
        "title": "Color Preferences"
    })
    
    # Generate HTML
    config.generate_html("test_data/demo_advanced_features.html")
    
    print(f"✓ Generated advanced features demo")
    print(f"  - Custom mini metrics: {len(config.config['miniMetrics'])}")
    print(f"  - Custom charts: {len(config.config['chartTypes'])}")
    print(f"  - File: test_data/demo_advanced_features.html")
    print()

def main():
    """Run all demos"""
    print("Data Explorer Demo Suite")
    print("=" * 50)
    print("This script demonstrates various configurations and use cases")
    print("for the modular data explorer system.")
    print()
    
    try:
        # Run all demos
        demo_basic_usage()
        demo_custom_charts()
        demo_time_series()
        demo_large_dataset()
        demo_angle_data()
        demo_export_config()
        demo_advanced_features()
        
        print("=" * 50)
        print("All demos completed successfully! 🎉")
        print()
        print("Generated demo files:")
        
        # List all generated files
        demo_files = [
            "test_data/demo_basic_numerical.html",
            "test_data/demo_custom_charts.html",
            "test_data/demo_time_series.html",
            "test_data/demo_large_dataset.html",
            "test_data/demo_angle_data.html",
            "test_data/demo_export_config.html",
            "test_data/demo_advanced_features.html",
            "test_data/demo_config.json"
        ]
        
        for file_path in demo_files:
            if Path(file_path).exists():
                if file_path.endswith('.html'):
                    size_mb = Path(file_path).stat().st_size / (1024 * 1024)
                    print(f"  - {file_path}: {size_mb:.1f} MB")
                else:
                    print(f"  - {file_path}")
        
        print()
        print("You can now open these HTML files in a browser to explore:")
        print("  - Basic numerical data exploration")
        print("  - Custom chart configurations")
        print("  - Time series analysis")
        print("  - Large dataset performance")
        print("  - Angular data visualization")
        print("  - Configuration export/reuse")
        print("  - Advanced features showcase")
        print()
        print("Each demo shows different aspects of the system's capabilities!")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
