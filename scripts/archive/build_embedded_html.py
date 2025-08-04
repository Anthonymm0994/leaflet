#!/usr/bin/env python3
"""
Build script to embed Arrow data into the HTML file as base64.
This creates a fully self-contained HTML file that can run offline.
"""

import base64
import os
import sys
import gzip
from pathlib import Path

def embed_arrow_data(html_file, arrow_file, output_file):
    """
    Embed Arrow data into HTML file as base64.
    
    Args:
        html_file: Path to the HTML template file
        arrow_file: Path to the Arrow data file
        output_file: Path to the output HTML file
    """
    print(f"Building embedded HTML file...")
    print(f"HTML template: {html_file}")
    print(f"Arrow data: {arrow_file}")
    print(f"Output: {output_file}")
    
    # Read the HTML template
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Read and encode the Arrow file
    with open(arrow_file, 'rb') as f:
        arrow_data = f.read()
    
    # Get file size info
    original_size = len(arrow_data)
    print(f"\nArrow file size: {original_size:,} bytes ({original_size / 1024 / 1024:.2f} MB)")
    
    # Option 1: Direct base64 encoding (larger but simpler)
    encoded_data = base64.b64encode(arrow_data).decode('ascii')
    encoded_size = len(encoded_data)
    print(f"Base64 encoded size: {encoded_size:,} bytes ({encoded_size / 1024 / 1024:.2f} MB)")
    
    # Option 2: Compress then base64 encode (smaller but requires decompression)
    compressed_data = gzip.compress(arrow_data, compresslevel=9)
    compressed_encoded = base64.b64encode(compressed_data).decode('ascii')
    compressed_size = len(compressed_encoded)
    print(f"Compressed + base64 size: {compressed_size:,} bytes ({compressed_size / 1024 / 1024:.2f} MB)")
    print(f"Compression ratio: {compressed_size / encoded_size:.2%}")
    
    # Find the placeholder in the HTML
    placeholder = '<!-- Base64 encoded Arrow data will be inserted here -->'
    
    if placeholder not in html_content:
        print("\nError: Could not find data placeholder in HTML file!")
        return False
    
    # For now, use direct encoding for simplicity
    # In production, you might want to use compression and add decompression logic
    html_content = html_content.replace(placeholder, encoded_data)
    
    # Write the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    output_size = os.path.getsize(output_file)
    print(f"\nOutput HTML file size: {output_size:,} bytes ({output_size / 1024 / 1024:.2f} MB)")
    print(f"Successfully created: {output_file}")
    
    return True

def embed_arrow_data_compressed(html_file, arrow_file, output_file):
    """
    Embed compressed Arrow data into HTML file as base64.
    
    Args:
        html_file: Path to the HTML template file
        arrow_file: Path to the Arrow data file
        output_file: Path to the output HTML file
    """
    print(f"Building embedded HTML file with compression...")
    print(f"HTML template: {html_file}")
    print(f"Arrow data: {arrow_file}")
    print(f"Output: {output_file}")
    
    # Read the HTML template
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Read and encode the Arrow file
    with open(arrow_file, 'rb') as f:
        arrow_data = f.read()
    
    # Get file size info
    original_size = len(arrow_data)
    print(f"\nArrow file size: {original_size:,} bytes ({original_size / 1024 / 1024:.2f} MB)")
    
    # Compress then base64 encode
    compressed_data = gzip.compress(arrow_data, compresslevel=9)
    compressed_encoded = base64.b64encode(compressed_data).decode('ascii')
    compressed_size = len(compressed_encoded)
    print(f"Compressed + base64 size: {compressed_size:,} bytes ({compressed_size / 1024 / 1024:.2f} MB)")
    print(f"Compression ratio: {original_size / compressed_size:.2f}x")
    
    # Find the placeholder in the HTML
    placeholder = '<!-- Base64 encoded compressed Arrow data will be inserted here -->'
    
    if placeholder not in html_content:
        print("\nError: Could not find data placeholder in HTML file!")
        return False
    
    # Replace with compressed data
    html_content = html_content.replace(placeholder, compressed_encoded)
    
    # Write the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    output_size = os.path.getsize(output_file)
    print(f"\nOutput HTML file size: {output_size:,} bytes ({output_size / 1024 / 1024:.2f} MB)")
    print(f"Successfully created: {output_file}")
    
    return True

def main():
    """Main function to build the embedded HTML files."""
    # Define file paths
    script_dir = Path(__file__).parent
    arrow_file = script_dir / 'data' / 'test_large_complex.arrow'
    
    # Build uncompressed version
    html_file = script_dir / 'data-explorer.html'
    output_file = script_dir / 'data-explorer-embedded.html'
    
    # Check if files exist
    if not html_file.exists():
        print(f"Error: HTML template file not found: {html_file}")
        sys.exit(1)
    
    if not arrow_file.exists():
        print(f"Error: Arrow data file not found: {arrow_file}")
        sys.exit(1)
    
    print("=== Building uncompressed version ===")
    success1 = embed_arrow_data(html_file, arrow_file, output_file)
    
    # Build compressed version
    print("\n=== Building compressed version ===")
    html_file_compressed = script_dir / 'data-explorer-compressed.html'
    output_file_compressed = script_dir / 'data-explorer-embedded-compressed.html'
    
    if html_file_compressed.exists():
        success2 = embed_arrow_data_compressed(html_file_compressed, arrow_file, output_file_compressed)
    else:
        print(f"Skipping compressed version - template not found: {html_file_compressed}")
        success2 = True
    
    if success1 and success2:
        print("\n✅ Build complete!")
        print(f"\nYou can now open either:")
        print(f"  - {output_file} (larger but simpler)")
        print(f"  - {output_file_compressed} (smaller with compression)")
        print("\nBoth files will work completely offline with no external dependencies.")
    else:
        print("\n❌ Build failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()