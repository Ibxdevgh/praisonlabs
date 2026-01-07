/**
 * Browser Console Script to Extract Spline URL from DICH Fashion Website
 * 
 * INSTRUCTIONS:
 * 1. Open https://dich-fashion.webflow.io/ in your browser
 * 2. Press F12 to open Developer Tools
 * 3. Go to the Console tab
 * 4. Paste this entire script and press Enter
 * 5. The Spline URL will be displayed in the console
 */

(function() {
    console.log('🔍 Searching for Spline URLs...');
    
    // Method 1: Search in HTML for data-spline-url attributes
    const splineElements = document.querySelectorAll('[data-spline-url], [data-animation-type="spline"]');
    console.log('Found ' + splineElements.length + ' Spline elements in HTML');
    
    splineElements.forEach((el, i) => {
        const url = el.getAttribute('data-spline-url') || el.getAttribute('url');
        if (url) {
            console.log('✓ Found Spline URL #' + (i + 1) + ':', url);
        }
    });
    
    // Method 2: Search for spline-viewer elements
    const viewers = document.querySelectorAll('spline-viewer');
    console.log('Found ' + viewers.length + ' spline-viewer elements');
    
    viewers.forEach((viewer, i) => {
        const url = viewer.getAttribute('url') || viewer.getAttribute('src');
        if (url) {
            console.log('✓ Found spline-viewer URL #' + (i + 1) + ':', url);
        }
    });
    
    // Method 3: Search in script tags
    const scripts = document.querySelectorAll('script');
    let foundInScripts = false;
    scripts.forEach(script => {
        const content = script.textContent || script.innerHTML;
        const splineMatches = content.match(/https?:\/\/[^\s"']+\.splinecode/g);
        if (splineMatches) {
            splineMatches.forEach(url => {
                console.log('✓ Found Spline URL in script:', url);
                foundInScripts = true;
            });
        }
    });
    
    // Method 4: Check Network requests (requires page reload)
    console.log('\n📡 To find URLs from network requests:');
    console.log('1. Go to Network tab');
    console.log('2. Filter by "spline" or ".splinecode"');
    console.log('3. Reload the page');
    console.log('4. Look for requests to .splinecode files');
    
    // Method 5: Check window objects
    if (window.Application) {
        console.log('✓ Application API found');
    }
    
    // Collect all found URLs
    const allUrls = [];
    splineElements.forEach(el => {
        const url = el.getAttribute('data-spline-url') || el.getAttribute('url');
        if (url) allUrls.push(url);
    });
    viewers.forEach(viewer => {
        const url = viewer.getAttribute('url') || viewer.getAttribute('src');
        if (url) allUrls.push(url);
    });
    
    if (allUrls.length > 0) {
        console.log('\n✅ SUMMARY - Found ' + allUrls.length + ' Spline URL(s):');
        allUrls.forEach((url, i) => {
            console.log((i + 1) + '. ' + url);
        });
        console.log('\n📋 Copy one of these URLs and use it in test-spline.html');
    } else {
        console.log('\n⚠️ No Spline URLs found in HTML. Try checking the Network tab after page reload.');
    }
    
    return allUrls;
})();

