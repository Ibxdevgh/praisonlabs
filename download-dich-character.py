#!/usr/bin/env python3
"""
Script to download Spline character from DICH Fashion website
Tries multiple methods to download the .splinecode file
"""

import requests
import sys
import os
from urllib.parse import urlparse

def download_spline_file(url, output_filename=None):
    """
    Attempt to download a Spline .splinecode file
    """
    if not output_filename:
        # Extract filename from URL
        parsed = urlparse(url)
        output_filename = os.path.basename(parsed.path) or "spline-character.splinecode"
    
    print(f"Attempting to download: {url}")
    print(f"Output file: {output_filename}")
    print("-" * 60)
    
    # Method 1: Standard request with headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://dich-fashion.webflow.io/',
        'Origin': 'https://dich-fashion.webflow.io'
    }
    
    try:
        print("Method 1: Standard request with headers...")
        response = requests.get(url, headers=headers, stream=True, timeout=30)
        response.raise_for_status()
        
        if response.status_code == 200:
            file_size = len(response.content)
            print(f"✓ Success! File size: {file_size:,} bytes")
            
            with open(output_filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ Saved to: {output_filename}")
            return True
        else:
            print(f"✗ Failed with status: {response.status_code}")
    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP Error: {e}")
        if e.response.status_code == 403:
            print("  → 403 Forbidden - File is protected")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Method 2: Try with session (maintains cookies)
    try:
        print("\nMethod 2: Using session with cookies...")
        session = requests.Session()
        session.headers.update(headers)
        
        # First visit the main page to get cookies
        session.get('https://dich-fashion.webflow.io/', timeout=10)
        
        response = session.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        if response.status_code == 200:
            file_size = len(response.content)
            print(f"✓ Success! File size: {file_size:,} bytes")
            
            with open(output_filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ Saved to: {output_filename}")
            return True
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Method 3: Try without referrer/origin
    try:
        print("\nMethod 3: Simple request without referrer...")
        simple_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=simple_headers, stream=True, timeout=30)
        response.raise_for_status()
        
        if response.status_code == 200:
            file_size = len(response.content)
            print(f"✓ Success! File size: {file_size:,} bytes")
            
            with open(output_filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ Saved to: {output_filename}")
            return True
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("All download methods failed.")
    print("\nAlternative methods:")
    print("1. Use browser Developer Tools:")
    print("   - Open Network tab")
    print("   - Filter by '.splinecode'")
    print("   - Right-click the file → Save As")
    print("\n2. Use browser extension:")
    print("   - Install a download manager extension")
    print("   - It may bypass some restrictions")
    print("\n3. Use spline-viewer to load, then inspect:")
    print("   - The file may be cached in browser")
    print("   - Check browser cache folder")
    
    return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python download-dich-character.py <SPLINE_URL>")
        print("\nExample:")
        print("  python download-dich-character.py https://prod.spline.design/.../scene.splinecode")
        print("\nTo find the URL:")
        print("  1. Open https://dich-fashion.webflow.io/")
        print("  2. Press F12 → Network tab")
        print("  3. Filter by 'spline'")
        print("  4. Reload page and find .splinecode file")
        sys.exit(1)
    
    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = download_spline_file(url, output_file)
    
    if success:
        print("\n" + "=" * 60)
        print("SUCCESS! Character downloaded.")
        print("You can now use this file locally in your project.")
    else:
        print("\n" + "=" * 60)
        print("Download failed. The file may be protected.")
        print("Try using browser Developer Tools method instead.")

if __name__ == "__main__":
    main()

