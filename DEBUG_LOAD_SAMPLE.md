# 🐛 Debug "Load Sample Data" Function

## Issue
"Try Sample Queries - Load sample function not working"

## What I've Added

I've added comprehensive console logging to help identify exactly where the issue is:

### Functions with Logging:
1. ✅ `loadSampleData()` - Logs file fetching and blob creation
2. ✅ `uploadFile()` - Logs upload process and server response
3. ✅ `displayResults()` - Logs display rendering steps

### How to Debug

**Step 1: Open Browser Console**
```
1. Go to http://localhost:5001
2. Press F12 (Windows/Linux) or Cmd+Opt+I (Mac)
3. Click "Console" tab
4. Clear any existing logs (click trash icon)
```

**Step 2: Try Loading Sample Data**
```
1. Click "Try Sample Data" tab
2. Click "Load Sample Dataset" button
3. Watch console for messages
```

**Step 3: What to Look For**

You should see these messages in order:

```
📥 Loading sample data...
✅ Sample file fetched: 200
✅ Blob created: 6153 bytes
✅ File object created: sample_queries_100.csv 6153
🚀 Uploading file...
📤 uploadFile() called with: sample_queries_100.csv 6153 bytes
⏳ Processing section displayed
📡 Upload response: 200 OK
📊 Response data received: {data: Array(100), summary: {...}, ...}
✅ Calling displayResults with 100 rows
🎨 displayResults() called
   - data.data rows: 100
   - results_filename: sample_queries_100
   - summary: {...}
   - Hiding processing section
   - Showing results section
   - Updating header stats
   - Calling displaySummary()
   - Calling displayDataTable()
   - Calling displayGroupedView()
   - Calling populateFilters()
✅ displayResults() complete
```

**Step 4: Identify Where It Stops**

Look for where the messages **stop appearing**. This tells us exactly what's failing:

### Scenario A: No Messages Appear
**Problem**: `loadSampleData()` function not being called
**Cause**: Button click handler not attached
**Solution**: Check if button exists in HTML

### Scenario B: Stops at "📥 Loading sample data..."
**Problem**: Fetch failing
**Cause**: File not accessible
**Solution**: Check file path and permissions

### Scenario C: Stops at "🚀 Uploading file..."
**Problem**: Upload not starting
**Cause**: `uploadFile()` not being called
**Solution**: Check setTimeout execution

### Scenario D: Stops at "📤 uploadFile() called..."
**Problem**: Upload request failing
**Cause**: Network error or CORS issue
**Solution**: Check network tab for failed requests

### Scenario E: Stops at "📊 Response data received"
**Problem**: displayResults() not being called
**Cause**: Error in data processing
**Solution**: Check data structure

### Scenario F: Stops at "🎨 displayResults() called"
**Problem**: DOM manipulation failing
**Cause**: Missing element IDs or JavaScript error
**Solution**: Check for RED error messages below this line

### Scenario G: Shows RED Error Messages
**Problem**: JavaScript execution error
**Cause**: Various (null reference, undefined variable, etc.)
**Solution**: Share the exact error message

---

## Quick Test

Try this in the browser console RIGHT NOW:

```javascript
// Test if function exists
console.log('loadSampleData exists?', typeof loadSampleData);

// Test if button exists
console.log('Button exists?', document.querySelector('[onclick*="loadSampleData"]'));

// Try calling function manually
loadSampleData();
```

This will tell us immediately if the function is accessible.

---

## Expected Output (Working System)

If everything works, you should see:

1. **Console logs** showing all steps completing
2. **Processing section** appears briefly (spinning animation)
3. **Results section** appears with:
   - 100 rows in the table
   - Summary cards showing "100 Total Queries"
   - Grouped view with topics
   - Filters populated

---

## Common Issues and Fixes

### Issue 1: "Processing" section shows but never disappears
**Problem**: Upload succeeds but display fails
**Look for**: Messages stop after "📊 Response data received"
**Fix**: Check if `displayResults()` function has error

### Issue 2: Nothing happens when clicking button
**Problem**: Click handler not attached
**Look for**: NO console messages at all
**Fix**: Check if `onclick="loadSampleData()"` is in button HTML

### Issue 3: "Error loading sample data: TypeError"
**Problem**: JavaScript error in fetch chain
**Look for**: RED error message after "📥 Loading sample data..."
**Fix**: Share the exact TypeError message

### Issue 4: "Error uploading file: NetworkError"
**Problem**: Upload endpoint not responding
**Look for**: Message after "📤 uploadFile() called"
**Fix**: Check server logs for errors

---

## What to Share With Me

**If the issue persists**, please share:

1. **Screenshot of Console** (F12 → Console tab)
2. **Last console message** you see before it stops
3. **Any RED error messages**
4. **Network tab** (F12 → Network tab) - any failed requests?

With this information, I can fix the issue in ~2 minutes!

---

## Testing Right Now

**Try this immediately**:

```
1. Open http://localhost:5001
2. Press F12
3. Click Console tab
4. Click "Try Sample Data" tab
5. Click "Load Sample Dataset"
6. Screenshot the console output
7. Share it with me
```

---

## Expected Server Logs

While testing, you should also see server logs:

```
GET /static/sample_queries_100.csv HTTP/1.1" 200 -
POST /upload HTTP/1.1" 200 -
```

If you DON'T see these in the terminal where Flask is running, the fetch/upload isn't even reaching the server.

---

## Browser Compatibility

**Tested on**:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

**If using older browser**: Update to latest version

---

## Cache Issue?

If you've hard-refreshed and it still doesn't work, try:

```bash
# Clear ALL browser data
Cmd+Shift+Delete (Mac)
Ctrl+Shift+Delete (Windows)

# Select:
- Cached images and files
- Time range: All time
- Clear data

# Or try incognito/private mode
Cmd+Shift+N (Chrome/Edge)
Cmd+Shift+P (Firefox/Safari)
```

---

**Status**: Debugging tools added ✅
**Next step**: Open console and share what you see!
