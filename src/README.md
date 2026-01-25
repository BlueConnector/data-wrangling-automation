# Web-Based Scraping Exercise

Interactive web application for learning adaptive web scraping with clear frontend/backend separation.

## Architecture

```
┌─────────────────────────────────────────┐
│          Frontend (Browser)             │
│  HTML + CSS + JavaScript                │
│  - User interface                       │
│  - Step-by-step tutorial                │
│  - Results visualization                │
└──────────────┬──────────────────────────┘
               │ HTTP/REST API
               │ (JSON)
┌──────────────▼──────────────────────────┐
│        Backend (Python Flask)           │
│  - REST API endpoints                   │
│  - ScraperEngine                        │
│  - BeautifulSoup scraping logic         │
└──────────────┬──────────────────────────┘
               │
         ┌─────▼──────┐
         │   Data     │
         │ selectors  │
         │ HTML files │
         └────────────┘
```

## Directory Structure

```
src/
├── backend/
│   ├── app.py              # Flask API server
│   ├── scraper.py          # Scraping engine logic
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html          # Main HTML page
│   ├── styles.css          # Styling
│   ├── api.js              # API client (backend communication)
│   └── app.js              # Frontend application logic
└── README.md               # This file
```

## Setup & Installation

### 1. Install Backend Dependencies

```bash
cd src/backend
pip install -r requirements.txt
```

### 2. Start the Backend Server

```bash
python src/backend/app.py
```

You should see:
```
🚀 Starting Web Scraping Exercise Backend
Backend API running at: http://localhost:5000
Frontend available at: http://localhost:5000
```

### 3. Open Frontend

Open your browser and navigate to:
```
http://localhost:5000
```

The frontend will automatically connect to the backend API.

## How It Works

### Frontend (JavaScript → Python Communication)

The frontend uses the `ScraperAPI` class in `api.js` to communicate with the Python backend:

```javascript
// Example: Execute scraping
const result = await ScraperAPI.scrape(
    '#statistics-table tbody tr',  // selector
    'v1',                           // version
    'ID selector'                   // name
);

console.log(result.data);  // Scraped data from Python
```

### Backend (Python Processing)

The Flask backend provides REST API endpoints:

```python
@app.route('/api/scrape', methods=['POST'])
def scrape():
    # Receives: { selector, version, selector_name }
    # Returns: { success, data, validation, ... }
    result = scraper_engine.scrape(selector, version, selector_name)
    return jsonify(result)
```

The `ScraperEngine` class handles actual scraping using BeautifulSoup:

```python
def scrape(self, selector, version, selector_name):
    soup = BeautifulSoup(html_content, 'html.parser')
    rows = soup.select(selector)
    data = self._parse_rows(rows)
    return {'success': True, 'data': data}
```

## API Endpoints

### GET `/api/health`
Check if backend is running
```json
Response: { "status": "healthy" }
```

### GET `/api/selectors`
Get available selectors from configuration
```json
Response: {
  "success": true,
  "selectors": [...]
}
```

### GET `/api/html-samples`
Get HTML samples for each version
```json
Response: {
  "success": true,
  "samples": {
    "v1": "<html>...",
    "v2": "<html>...",
    "v3": "<html>..."
  }
}
```

### POST `/api/scrape`
Execute scraping operation
```json
Request: {
  "selector": "#statistics-table tbody tr",
  "version": "v1",
  "selector_name": "ID selector"
}

Response: {
  "success": true,
  "data": [...],
  "rows_found": 8,
  "validation": {...}
}
```

### POST `/api/test-selector`
Test if selector finds elements
```json
Request: {
  "selector": "#statistics-table tbody tr",
  "version": "v1"
}

Response: {
  "success": true,
  "found": true,
  "count": 8
}
```

### POST `/api/validate`
Validate extracted data
```json
Request: {
  "data": [...]
}

Response: {
  "valid": true,
  "checks": {...},
  "issues": []
}
```

## Development

### Backend Development

The backend is pure Python with clear separation:
- `app.py` - API routes only
- `scraper.py` - Business logic only

To modify scraping logic, edit `scraper.py`. API stays unchanged.

### Frontend Development

The frontend has clear separation:
- `index.html` - Structure
- `styles.css` - Styling  
- `api.js` - Backend communication only
- `app.js` - UI logic only

To change UI behavior, edit `app.js`. API calls stay in `api.js`.

## Testing

### Test Backend Separately

```bash
# In Python shell or script
from src.backend.scraper import ScraperEngine

engine = ScraperEngine()
result = engine.scrape('#statistics-table tbody tr', 'v1', 'Test')
print(result)
```

### Test API Endpoints

```bash
# Using curl
curl http://localhost:5000/api/health

curl -X POST http://localhost:5000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{"selector":"#statistics-table tbody tr","version":"v1","selector_name":"Test"}'
```

### Test Frontend

Open browser console and test API client:
```javascript
ScraperAPI.checkHealth().then(console.log);
ScraperAPI.getSelectors().then(console.log);
```

## Troubleshooting

### Backend won't start
- Check if port 5000 is already in use
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.8+)

### Frontend shows "Backend offline"
- Ensure backend is running on port 5000
- Check browser console for CORS errors
- Verify firewall isn't blocking localhost:5000

### Scraping returns no data
- Check that data files exist in `data/` directory
- Verify HTML files are in correct location
- Check backend logs for errors

## Production Deployment

For production use:

1. **Remove CORS for security** (only allow specific origins)
2. **Add authentication** (API keys, JWT tokens)
3. **Use production WSGI server** (Gunicorn, uWSGI instead of Flask dev server)
4. **Add rate limiting** (prevent abuse)
5. **Implement caching** (reduce repeated scraping)
6. **Add logging** (structured logs for monitoring)

Example production config:
```python
# Use Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.backend.app:app
```

## Learning Objectives

This architecture teaches:
- ✅ Frontend/backend separation
- ✅ REST API design
- ✅ Asynchronous JavaScript (fetch, promises)
- ✅ Python web frameworks (Flask)
- ✅ Web scraping with BeautifulSoup
- ✅ Data validation and error handling

## Next Steps

1. Complete the interactive tutorial in the browser
2. Examine `api.js` to see how frontend calls Python
3. Examine `scraper.py` to see BeautifulSoup in action
4. Modify selectors in `data/selectors.csv`
5. Add your own HTML samples to test against

## Support

If you encounter issues:
1. Check backend logs in terminal
2. Check browser console for frontend errors
3. Verify all files are in correct directories
4. Ensure dependencies are installed

Happy scraping! 🕷️