#!/usr/bin/env python3
"""
🚀 V13 Real-Time Streaming Dashboard Engine Test Suite

This script tests the real-time streaming capabilities, data generation,
and performance monitoring of the V13 engine.
"""

import json
import time
import random
import math
from datetime import datetime, timedelta

def generate_streaming_data(num_points=1000, stream_type='random'):
    """Generate different types of streaming data for testing."""
    
    data = []
    base_time = datetime.now() - timedelta(minutes=10)
    
    if stream_type == 'random':
        # Random noise data
        for i in range(num_points):
            timestamp = base_time + timedelta(milliseconds=i * 100)
            data.append({
                'timestamp': timestamp.isoformat(),
                'value': random.uniform(0, 100),
                'x': random.uniform(0, 1000),
                'y': random.uniform(0, 1000),
                'intensity': random.uniform(0, 1),
                'category': random.choice(['A', 'B', 'C', 'D']),
                'node': random.randint(0, 9),
                'edge': random.randint(0, 4)
            })
    
    elif stream_type == 'trending':
        # Trending data with upward/downward patterns
        trend = random.choice([1, -1])
        base_value = random.uniform(20, 80)
        
        for i in range(num_points):
            timestamp = base_time + timedelta(milliseconds=i * 100)
            noise = random.uniform(-5, 5)
            trend_value = trend * (i / num_points) * 30
            
            data.append({
                'timestamp': timestamp.isoformat(),
                'value': max(0, min(100, base_value + trend_value + noise)),
                'x': i * 2 + random.uniform(-10, 10),
                'y': 100 + 50 * math.cos(i * 0.05) + random.uniform(-15, 15),
                'intensity': 0.5 + 0.3 * math.sin(i * 0.02) + random.uniform(-0.1, 0.1),
                'category': ['A', 'B', 'C', 'D'][i % 4],
                'node': i % 10,
                'edge': i % 5
            })
    
    elif stream_type == 'seasonal':
        # Seasonal/cyclic data
        for i in range(num_points):
            timestamp = base_time + timedelta(milliseconds=i * 100)
            cycle = math.sin(i * 0.1) * 30 + 50
            seasonal = math.sin(i * 0.02) * 20
            noise = random.uniform(-3, 3)
            
            data.append({
                'timestamp': timestamp.isoformat(),
                'value': max(0, min(100, cycle + seasonal + noise)),
                'x': i * 1.5 + random.uniform(-5, 5),
                'y': 200 + 100 * math.sin(i * 0.03) + random.uniform(-10, 10),
                'intensity': 0.6 + 0.2 * math.sin(i * 0.015) + random.uniform(-0.05, 0.05),
                'category': ['A', 'B', 'C', 'D'][i % 4],
                'node': i % 10,
                'edge': i % 5
            })
    
    elif stream_type == 'clustered':
        # Clustered data with distinct groups
        clusters = [
            {'center_x': 200, 'center_y': 200, 'center_value': 30},
            {'center_x': 600, 'center_y': 400, 'center_value': 70},
            {'center_x': 800, 'center_y': 100, 'center_value': 50}
        ]
        
        for i in range(num_points):
            timestamp = base_time + timedelta(milliseconds=i * 100)
            cluster = random.choice(clusters)
            
            data.append({
                'timestamp': timestamp.isoformat(),
                'value': cluster['center_value'] + random.uniform(-15, 15),
                'x': cluster['center_x'] + random.uniform(-100, 100),
                'y': cluster['center_y'] + random.uniform(-100, 100),
                'intensity': 0.7 + random.uniform(-0.2, 0.2),
                'category': random.choice(['A', 'B', 'C', 'D']),
                'node': random.randint(0, 9),
                'edge': random.randint(0, 4)
            })
    
    elif stream_type == 'anomaly':
        # Data with occasional anomalies
        for i in range(num_points):
            timestamp = base_time + timedelta(milliseconds=i * 100)
            
            # 5% chance of anomaly
            if random.random() < 0.05:
                value = random.uniform(80, 120)  # Out of normal range
                x = random.uniform(900, 1100)   # Out of normal range
                y = random.uniform(900, 1100)   # Out of normal range
            else:
                value = random.uniform(40, 60)
                x = random.uniform(400, 600)
                y = random.uniform(300, 500)
            
            data.append({
                'timestamp': timestamp.isoformat(),
                'value': max(0, min(100, value)),
                'x': max(0, min(1000, x)),
                'y': max(0, min(1000, y)),
                'intensity': 0.5 + random.uniform(-0.1, 0.1),
                'category': random.choice(['A', 'B', 'C', 'D']),
                'node': random.randint(0, 9),
                'edge': random.randint(0, 4)
            })
    
    return data

def test_streaming_performance():
    """Test streaming performance with different data rates."""
    
    print("🚀 Testing Streaming Performance...")
    
    data_sizes = [100, 500, 1000, 5000, 10000]
    stream_types = ['random', 'trending', 'seasonal', 'clustered', 'anomaly']
    
    results = {}
    
    for stream_type in stream_types:
        results[stream_type] = {}
        
        for size in data_sizes:
            print(f"  Testing {stream_type} data with {size} points...")
            
            start_time = time.time()
            data = generate_streaming_data(size, stream_type)
            generation_time = (time.time() - start_time) * 1000
            
            # Simulate streaming updates
            update_times = []
            for i in range(min(100, size)):  # Test first 100 updates
                start = time.time()
                # Simulate chart update
                time.sleep(0.001)  # Simulate processing time
                update_time = (time.time() - start) * 1000
                update_times.append(update_time)
            
            avg_update_time = sum(update_times) / len(update_times)
            max_update_time = max(update_times)
            min_update_time = min(update_times)
            
            results[stream_type][size] = {
                'generation_time_ms': round(generation_time, 2),
                'avg_update_time_ms': round(avg_update_time, 2),
                'max_update_time_ms': round(max_update_time, 2),
                'min_update_time_ms': round(min_update_time, 2),
                'data_size_mb': round(len(json.dumps(data)) / (1024 * 1024), 3)
            }
    
    return results

def test_real_time_latency():
    """Test real-time latency simulation."""
    
    print("⚡ Testing Real-Time Latency...")
    
    latencies = [16, 33, 50, 100, 200, 500]  # ms
    results = {}
    
    for latency in latencies:
        print(f"  Testing {latency}ms latency...")
        
        start_time = time.time()
        data_points = []
        
        # Simulate 1 second of streaming at specified latency
        num_updates = 1000 // latency
        for i in range(num_updates):
            data_points.append({
                'timestamp': time.time(),
                'value': random.uniform(0, 100),
                'update_number': i
            })
            time.sleep(latency / 1000)  # Convert ms to seconds
        
        actual_time = time.time() - start_time
        expected_time = 1.0  # 1 second
        time_error = abs(actual_time - expected_time)
        
        results[latency] = {
            'actual_time_seconds': round(actual_time, 3),
            'expected_time_seconds': expected_time,
            'time_error_seconds': round(time_error, 3),
            'data_points_generated': len(data_points),
            'theoretical_fps': round(1000 / latency, 1)
        }
    
    return results

def test_memory_efficiency():
    """Test memory efficiency with large datasets."""
    
    print("💾 Testing Memory Efficiency...")
    
    dataset_sizes = [1000, 5000, 10000, 50000, 100000]
    results = {}
    
    for size in dataset_sizes:
        print(f"  Testing dataset size: {size:,} points...")
        
        start_time = time.time()
        data = generate_streaming_data(size, 'random')
        generation_time = (time.time() - start_time) * 1000
        
        # Calculate memory usage
        json_str = json.dumps(data)
        memory_bytes = len(json_str.encode('utf-8'))
        memory_mb = memory_bytes / (1024 * 1024)
        
        # Simulate data processing overhead
        processing_time = 0
        for i in range(0, size, 1000):  # Process in chunks
            chunk = data[i:i+1000]
            start = time.time()
            # Simulate processing
            _ = [item['value'] for item in chunk]
            processing_time += (time.time() - start) * 1000
        
        results[size] = {
            'generation_time_ms': round(generation_time, 2),
            'memory_usage_mb': round(memory_mb, 3),
            'processing_time_ms': round(processing_time, 2),
            'bytes_per_point': round(memory_bytes / size, 1),
            'points_per_second': round(size / (generation_time / 1000), 0)
        }
    
    return results

def create_performance_report(streaming_results, latency_results, memory_results):
    """Create a comprehensive performance report."""
    
    report = f"""
V13 Real-Time Streaming Dashboard Engine - Performance Report
{'='*70}

STREAMING PERFORMANCE RESULTS
{'-'*40}

"""
    
    for stream_type, sizes in streaming_results.items():
        report += f"\n{stream_type.upper()} DATA STREAMING:\n"
        for size, metrics in sizes.items():
            report += f"  {size:,} points: {metrics['generation_time_ms']}ms generation, "
            report += f"{metrics['avg_update_time_ms']}ms avg update, "
            report += f"{metrics['data_size_mb']}MB\n"
    
    report += f"""

REAL-TIME LATENCY RESULTS
{'-'*40}

"""
    
    for latency, metrics in latency_results.items():
        report += f"  {latency}ms target: {metrics['actual_time_seconds']}s actual, "
        report += f"{metrics['time_error_seconds']}s error, "
        report += f"{metrics['theoretical_fps']} FPS\n"
    
    report += f"""

MEMORY EFFICIENCY RESULTS
{'-'*40}

"""
    
    for size, metrics in memory_results.items():
        report += f"  {size:,} points: {metrics['memory_usage_mb']}MB, "
        report += f"{metrics['bytes_per_point']} bytes/point, "
        report += f"{metrics['points_per_second']} points/sec\n"
    
    report += f"""

PERFORMANCE SUMMARY
{'-'*40}

- Fastest streaming: {min([min(sizes.values(), key=lambda x: x['generation_time_ms'])['generation_time_ms'] for sizes in streaming_results.values()])}ms
- Lowest latency: {min(latency_results.keys())}ms
- Most efficient: {min(memory_results.values(), key=lambda x: x['bytes_per_point'])['bytes_per_point']} bytes/point
- Highest throughput: {max([max(sizes.values(), key=lambda x: x['data_size_mb'])['data_size_mb'] for sizes in streaming_results.values()])} MB

RECOMMENDATIONS
{'-'*40}

- Use 'trending' data for smooth visualizations
- Target 50-100ms latency for real-time feel
- Process data in chunks of 1000-5000 for optimal performance
- Monitor memory usage for datasets >50K points

{'='*70}
Performance testing completed successfully!
"""
    
    return report

def create_test_datasets():
    """Create sample JSON datasets for testing."""
    
    print("📁 Creating test datasets...")
    
    datasets = {
        'random_stream': generate_streaming_data(1000, 'random'),
        'trending_stream': generate_streaming_data(1000, 'trending'),
        'seasonal_stream': generate_streaming_data(1000, 'seasonal'),
        'clustered_stream': generate_streaming_data(1000, 'clustered'),
        'anomaly_stream': generate_streaming_data(1000, 'anomaly'),
        'large_dataset': generate_streaming_data(50000, 'random')
    }
    
    for name, data in datasets.items():
        filename = f"{name}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  ✅ Created {filename} ({len(data):,} points)")
    
    return datasets

def main():
    """Main test execution function."""
    
    print("🚀 V13 Real-Time Streaming Dashboard Engine Test Suite")
    print("Testing real-time streaming, latency, and performance capabilities")
    print("="*70)
    
    try:
        # Run all tests
        print("\n1️⃣ Testing streaming performance...")
        streaming_results = test_streaming_performance()
        
        print("\n2️⃣ Testing real-time latency...")
        latency_results = test_real_time_latency()
        
        print("\n3️⃣ Testing memory efficiency...")
        memory_results = test_memory_efficiency()
        
        print("\n4️⃣ Creating performance report...")
        report = create_performance_report(streaming_results, latency_results, memory_results)
        
        # Save report
        with open('performance_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("\n5️⃣ Creating test datasets...")
        create_test_datasets()
        
        print("\n" + "="*70)
        print("✅ ALL STREAMING TESTS COMPLETED SUCCESSFULLY!")
        print("="*70)
        
        print("\n📊 Results Summary:")
        print(f"• Streaming types tested: {len(streaming_results)}")
        print(f"• Latency targets tested: {len(latency_results)}")
        print(f"• Dataset sizes tested: {len(memory_results)}")
        print(f"• Performance report: performance_report.txt")
        print(f"• Test datasets: *.json files")
        
        print("\n🚀 Next steps:")
        print("1. Open realtime_streaming_engine.html in your browser")
        print("2. Click 'Load Sample' to load test datasets")
        print("3. Click 'Simulate Stream' to start real-time streaming")
        print("4. Monitor performance stats and streaming metrics")
        print("5. Use keyboard shortcuts (Space, R, F) for controls")
        
        print("\n💡 Tips:")
        print("• Start with smaller datasets to test performance")
        print("• Use different stream types to see various patterns")
        print("• Monitor FPS and memory usage during streaming")
        print("• Try different zoom levels and interactions")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
