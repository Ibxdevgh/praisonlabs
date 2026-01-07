# How to Download the DICH Fashion Spline Character

## Method 1: Browser Developer Tools (Easiest & Most Reliable)

1. **Open the DICH Fashion website:**
   - Go to https://dich-fashion.webflow.io/
   - Wait for the page to fully load

2. **Open Developer Tools:**
   - Press `F12` (or Right-click → Inspect)
   - Go to the **Network** tab

3. **Filter for Spline files:**
   - In the filter box, type: `spline` or `.splinecode`
   - Press Enter

4. **Reload the page:**
   - Press `F5` to reload
   - Watch the Network tab for requests

5. **Find the Spline file:**
   - Look for a file ending in `.splinecode`
   - It should show in the list of network requests

6. **Download the file:**
   - **Option A:** Right-click the file → **Open in new tab** → Right-click → **Save As**
   - **Option B:** Right-click the file → **Copy** → **Copy URL** → Paste in browser → **Save As**
   - **Option C:** Click the file → Go to **Headers** tab → Copy the **Request URL** → Paste in browser → **Save As**

## Method 2: Using the Helper HTML Tool

1. Open `download-dich-character.html` in your browser
2. Follow the instructions to find the Spline URL
3. Paste the URL and click "Download"
4. If CORS blocks it, use Method 1 instead

## Method 3: Using Python Script

1. First, find the Spline URL using Method 1
2. Run the Python script:
   ```bash
   python download-dich-character.py <SPLINE_URL>
   ```
3. Example:
   ```bash
   python download-dich-character.py https://prod.spline.design/abc123/scene.splinecode
   ```

## Method 4: Browser Cache (If Already Loaded)

If you've already viewed the character:

1. Open Developer Tools → **Application** tab (Chrome) or **Storage** tab (Firefox)
2. Go to **Cache Storage** or **Cache**
3. Look for the `.splinecode` file
4. Right-click → **Save As**

## Troubleshooting

### If you get 403 Forbidden:
- The file is protected by CORS
- Use **Method 1** (browser method) - it works because the browser has the right cookies/referrer
- The Python script may not work due to CORS restrictions

### If you can't find the file:
- Make sure you're filtering correctly in Network tab
- Try filtering by: `spline`, `.splinecode`, or `splinecode`
- Reload the page after setting the filter
- Check if the character is loaded via iframe (look for iframe requests)

### If the file downloads but won't load:
- Make sure it's a `.splinecode` file (not JSON or other format)
- Check the file size (should be several KB to MB)
- Try opening it in a text editor - it should start with binary data or encoded content

## After Downloading

Once you have the `.splinecode` file:

1. **Save it locally** in your project folder
2. **Update your HTML files:**
   - `index.htm` line 2401: Change the URL to point to your local file
   - `test-spline.html` line 199: Update the URL
3. **Or keep it on CDN:**
   - If the URL works, you can keep using the CDN URL
   - Just replace it with the DICH Fashion URL

## File Locations to Update

After downloading, update these files:

- `index.htm` - Line 2401
- `index-1.htm` - Line 2398  
- `test-spline.html` - Line 199

Replace the URL with either:
- Local path: `./dich-character.splinecode`
- Or the new CDN URL from DICH Fashion website

