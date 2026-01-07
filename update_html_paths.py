#!/usr/bin/env python3
"""
Script to update HTML files to use local paths instead of CDN URLs
"""
import re
import json
import os
from pathlib import Path
import urllib.parse

def normalize_url(url):
    """Normalize URL for comparison (decode URL encoding)"""
    return urllib.parse.unquote(url)

def get_local_filename(url):
    """Extract local filename from CDN URL"""
    parsed = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed.path)
    filename = urllib.parse.unquote(filename)
    if not filename or filename == '/':
        path_parts = [p for p in parsed.path.split('/') if p]
        if path_parts:
            filename = path_parts[-1]
    return filename

def update_html_file(filepath, url_mapping):
    """Update HTML file to replace CDN URLs with local paths"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        replacements = 0
        
        # Create a reverse mapping: normalized URL -> local file
        reverse_mapping = {}
        for cdn_url, local_file in url_mapping.items():
            normalized = normalize_url(cdn_url)
            if os.path.exists(local_file):
                reverse_mapping[normalized] = local_file
                # Also add the original URL
                reverse_mapping[cdn_url] = local_file
        
        # Replace URLs in various attributes
        # Pattern to match CDN URLs
        cdn_base = r'https://cdn\.prod\.website-files\.com/[^\s"\'\)]+'
        
        def replace_url(match):
            url = match.group(0)
            normalized = normalize_url(url)
            
            # Try exact match first
            if url in reverse_mapping:
                return reverse_mapping[url]
            # Try normalized match
            if normalized in reverse_mapping:
                return reverse_mapping[normalized]
            
            # Try to find by filename
            filename = get_local_filename(url)
            if filename and os.path.exists(filename):
                return filename
            
            return url  # Return original if no match
        
        # Replace in the entire content
        new_content = re.sub(cdn_base, replace_url, content)
        
        # Count replacements
        if new_content != original_content:
            # Count how many URLs were replaced
            original_urls = len(re.findall(cdn_base, original_content))
            new_urls = len(re.findall(cdn_base, new_content))
            replacements = original_urls - new_urls
            
            # Write updated content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, replacements
        
        return False, 0
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        import traceback
        traceback.print_exc()
        return False, 0

def main():
    # Load URL mapping
    if not os.path.exists('url_mapping.json'):
        print("Error: url_mapping.json not found. Run download_assets.py first.")
        return
    
    with open('url_mapping.json', 'r') as f:
        url_mapping = json.load(f)
    
    print(f"Loaded {len(url_mapping)} URL mappings\n")
    
    # Find all HTML files
    base_dir = Path(".")
    html_files = list(base_dir.glob("*.htm")) + list(base_dir.glob("*.html"))
    
    total_replacements = 0
    
    for html_file in html_files:
        print(f"Processing: {html_file.name}")
        updated, count = update_html_file(html_file, url_mapping)
        if updated:
            print(f"  Updated {count} URLs")
            total_replacements += count
        else:
            print(f"  No changes needed")
    
    print(f"\n{'=' * 60}")
    print(f"Total replacements: {total_replacements}")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    main()
