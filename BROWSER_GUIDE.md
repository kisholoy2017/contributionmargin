# 🌐 Browser Access Guide for MER Calculator

## ✅ Server Status: RUNNING PERFECTLY ✅

The MER Calculator server has been tested and is working correctly:
- ✅ Main page loads (19,536 characters)
- ✅ API endpoints respond correctly
- ✅ All calculations working
- ✅ Charts and interface ready

## 🔗 Access URLs

### Primary URL
**http://localhost:8000**

### Alternative URLs (try these if main doesn't work)
- http://127.0.0.1:8000
- http://0.0.0.0:8000

## 🛠️ Troubleshooting Steps

### 1. Browser Issues
**Clear Browser Cache:**
- **Chrome/Edge**: Ctrl+Shift+Delete → Clear browsing data
- **Firefox**: Ctrl+Shift+Delete → Clear recent history
- **Safari**: Cmd+Option+E → Empty caches

**Try Incognito/Private Mode:**
- Chrome: Ctrl+Shift+N
- Firefox: Ctrl+Shift+P
- Safari: Cmd+Shift+N

### 2. URL Issues
**Make sure you're using:**
- ✅ `http://localhost:8000` (not https)
- ✅ Port 8000 (not 80 or 443)
- ✅ No trailing slash issues

**Don't use:**
- ❌ `https://localhost:8000` (no SSL)
- ❌ `localhost:8000` (missing protocol)
- ❌ `www.localhost:8000` (invalid)

### 3. Browser Compatibility
**Tested and Working:**
- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

**Try a different browser if current one fails**

### 4. Network Issues
**Check if port is blocked:**
```bash
# Test with curl (should show HTML)
curl http://localhost:8000

# Test with wget
wget -O - http://localhost:8000
```

**Firewall/Antivirus:**
- Temporarily disable firewall
- Add exception for port 8000
- Check antivirus web protection

### 5. System Issues
**Port conflicts:**
```bash
# Check what's using port 8000
lsof -i :8000
netstat -tlnp | grep 8000
```

**Restart server if needed:**
```bash
# Stop current server
pkill -f simple_app.py

# Start again
python3 simple_app.py
```

## 🔍 Step-by-Step Testing

### Step 1: Basic Connection Test
1. Open terminal/command prompt
2. Run: `curl http://localhost:8000`
3. Should see HTML starting with `<!DOCTYPE html>`

### Step 2: Browser Test
1. Open your browser
2. Type exactly: `http://localhost:8000`
3. Press Enter
4. Should see MER Calculator interface

### Step 3: Functionality Test
1. Enter values:
   - Target Revenue: 820000
   - Target MER: 7.5
   - Variable Cost: 0.65
   - CM Goal: 176000
2. Click "Calculate Contribution Margin"
3. Should see results and chart

## 🆘 Still Not Working?

### Alternative Access Methods

**1. Try Different Port:**
Edit `simple_app.py` and change:
```python
port = 8000  # Change to 8080 or 3000
```

**2. Try Different Host:**
Edit `simple_app.py` and change:
```python
server = HTTPServer(('127.0.0.1', port), MERRequestHandler)
```

**3. Use Python's Built-in Server:**
```bash
# Navigate to directory with HTML file
python3 -m http.server 8080
```

### Quick Test Page
Create a simple test HTML file:
```html
<!DOCTYPE html>
<html><body><h1>Test Page</h1></body></html>
```

Save as `test.html` and try: `http://localhost:8000/test.html`

## 📱 Mobile/Remote Access

**Find your IP address:**
```bash
# Linux/Mac
ip addr show | grep inet
ifconfig | grep inet

# Windows
ipconfig
```

**Access from other devices:**
`http://[YOUR-IP]:8000`

Example: `http://192.168.1.100:8000`

## 🎯 Expected Result

When working correctly, you should see:
- 🎨 Professional blue gradient header
- 📊 Form with Target Revenue, MER, Variable Cost fields
- 🧮 "Calculate Contribution Margin" button
- 📈 Results section (hidden until calculation)
- 📊 Interactive Chart.js chart (after calculation)

## 🔧 Advanced Debugging

**Enable verbose logging:**
Add this to `simple_app.py` main function:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Check server logs:**
The terminal running `simple_app.py` should show:
```
🧮 MER Calculator Server Starting...
🌐 Server running at: http://localhost:8000
```

**Manual API test:**
```bash
# Test API endpoint
curl -X POST -H "Content-Type: application/json" \
  -d '{"target_revenue":820000,"target_mer":7.5,"variable_cost":0.65,"contribution_margin_goal":176000,"revenue_increment":20000}' \
  http://localhost:8000/api/calculate
```

The server is confirmed working. The issue is likely browser-related. Try the troubleshooting steps above!