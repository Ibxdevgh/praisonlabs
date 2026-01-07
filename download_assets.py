#!/usr/bin/env python3
"""
Script to download all missing assets from CDN and update HTML files
"""
import re
import os
import urllib.request
import urllib.parse
from pathlib import Path
from html.parser import HTMLParser
import json

class URLCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = set()
        self.cdn_base = "https://cdn.prod.website-files.com"
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Check data-src (lazy loaded images)
        if 'data-src' in attrs_dict:
            url = attrs_dict['data-src']
            if url.startswith('http'):
                self.urls.add(url)
        
        # Check src attributes
        if 'src' in attrs_dict:
            url = attrs_dict['src']
            if url.startswith('http'):
                self.urls.add(url)
        
        # Check data-spline-url (Spline 3D models)
        if 'data-spline-url' in attrs_dict:
            url = attrs_dict['data-spline-url']
            if url.startswith('http'):
                self.urls.add(url)
        
        # Check data-src for Lottie animations
        if 'data-src' in attrs_dict and attrs_dict.get('data-animation-type') == 'lottie':
            url = attrs_dict['data-src']
            if url.startswith('http'):
                self.urls.add(url)
        
        # Check content attributes (meta tags)
        if 'content' in attrs_dict:
            url = attrs_dict['content']
            if url.startswith('http') and ('.webp' in url or '.jpg' in url or '.png' in url):
                self.urls.add(url)

def extract_urls_from_file(filepath):
    """Extract all CDN URLs from an HTML file"""
    collector = URLCollector()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            collector.feed(content)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    
    # Also use regex to catch URLs in JavaScript code
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        # Find URLs in JavaScript strings
        pattern = r'https://cdn\.prod\.website-files\.com/[^\s"\'\)]+'
        matches = re.findall(pattern, content)
        collector.urls.update(matches)
    
    return collector.urls

def download_file(url, local_path):
    """Download a file from URL to local path"""
    try:
        # Create directory if it doesn't exist
        dir_path = os.path.dirname(local_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        
        # Download the file
        print(f"Downloading: {url}")
        urllib.request.urlretrieve(url, local_path)
        print(f"  [OK] Saved to: {local_path}")
        return True
    except Exception as e:
        print(f"  [ERROR] Error downloading {url}: {e}")
        return False

def get_filename_from_url(url):
    """Extract filename from URL"""
    parsed = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed.path)
    # Decode URL encoding
    filename = urllib.parse.unquote(filename)
    # If no filename, use the last part of the path
    if not filename or filename == '/':
        path_parts = [p for p in parsed.path.split('/') if p]
        if path_parts:
            filename = path_parts[-1]
        else:
            # Fallback: use a hash of the URL
            filename = url.split('/')[-1] or 'unknown_file'
    return filename

def main():
    base_dir = Path(".")
    html_files = list(base_dir.glob("*.htm")) + list(base_dir.glob("*.html"))
    
    all_urls = set()
    
    print("=" * 60)
    print("Extracting URLs from HTML files...")
    print("=" * 60)
    
    for html_file in html_files:
        print(f"\nProcessing: {html_file.name}")
        urls = extract_urls_from_file(html_file)
        all_urls.update(urls)
        print(f"  Found {len(urls)} unique URLs")
    
    print(f"\n{'=' * 60}")
    print(f"Total unique URLs found: {len(all_urls)}")
    print(f"{'=' * 60}\n")
    
    # Filter only CDN URLs
    cdn_urls = [url for url in all_urls if 'cdn.prod.website-files.com' in url]
    print(f"CDN URLs to download: {len(cdn_urls)}\n")
    
    # Download files
    downloaded = []
    failed = []
    
    for url in sorted(cdn_urls):
        filename = get_filename_from_url(url)
        local_path = base_dir / filename
        
        # Skip if file already exists
        if local_path.exists():
            print(f"Skipping (exists): {filename}")
            downloaded.append((url, str(local_path)))
            continue
        
        if download_file(url, local_path):
            downloaded.append((url, str(local_path)))
        else:
            failed.append(url)
    
    print(f"\n{'=' * 60}")
    print(f"Download Summary:")
    print(f"  Successfully downloaded: {len(downloaded)}")
    print(f"  Failed: {len(failed)}")
    print(f"{'=' * 60}\n")
    
    # Save mapping for HTML updates
    url_mapping = {url: get_filename_from_url(url) for url, _ in downloaded}
    
    with open('url_mapping.json', 'w') as f:
        json.dump(url_mapping, f, indent=2)
    
    print("URL mapping saved to url_mapping.json")
    
    if failed:
        print("\nFailed URLs:")
        for url in failed:
            print(f"  - {url}")

if __name__ == "__main__":
    main()

