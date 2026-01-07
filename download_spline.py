import urllib.request
import urllib.error

files = [
    ('https://cdn.prod.website-files.com/675835c7f4ae1fa1a79b3733/headless.splinecode', 'headless.splinecode'),
    ('https://cdn.prod.website-files.com/675835c7f4ae1fa1a79b3733/rock.splinecode', 'rock.splinecode')
]

for url, filename in files:
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        req.add_header('Referer', 'https://www.praisonlabs.com/')
        
        with urllib.request.urlopen(req) as response:
            with open(filename, 'wb') as f:
                f.write(response.read())
        print(f"Downloaded: {filename}")
    except urllib.error.HTTPError as e:
        print(f"Failed to download {filename}: HTTP {e.code} - {e.reason}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")


