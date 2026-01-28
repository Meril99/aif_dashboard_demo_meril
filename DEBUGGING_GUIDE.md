# Debugging Guide: Web App Data Display Issues

## Summary of Issues Found and Fixed

Your web application had **two critical issues** preventing data from displaying:

### 1. **Database Path Mismatch** ❌ FIXED
- **Problem**: `main_api.py` was looking for `ai_sandbox_PSA_13_Jan_2026.db`, but the actual database file was `ai_sandbox_PSA_16_Oct_2025_Cedric_v2.db`
- **Impact**: Backend couldn't connect to the database, so no data was available
- **Solution**: Updated the database path in `main_api.py` line 26
- **File Modified**: `backend/main_api.py`

### 2. **Missing Data Binding Configuration for Charts** ❌ FIXED
- **Problem**: The three chart components (Line Chart, Bar Chart, Radar Chart) were missing `data_binding` properties that tell the frontend where to fetch data from
- **Impact**: Charts had no API endpoint configured, so they couldn't fetch measure data
- **Solution**: Added `data_binding: { endpoint: "/measure/" }` to all three charts in the configuration JSON
- **Files Modified**: `frontend/src/data/ui_components.json`

---

## How to Debug Similar Issues in the Future

### Step 1: Check Backend Database Connection

The first step is always to verify the backend can access the database.

**Method A: Check Docker Backend Logs**
```powershell
# View backend container logs
docker logs web_app_output_jan_2026_float-backend

# Or follow logs in real-time
docker logs -f web_app_output_jan_2026_float-backend
```

**Method B: Test API Endpoints Directly**
```powershell
# Test if the /measure/ endpoint returns data
Invoke-WebRequest -Uri http://localhost:8000/measure/ -OutFile response.json
Get-Content response.json | ConvertFrom-Json | Measure-Object

# Check system health/status endpoint
Invoke-WebRequest -Uri http://localhost:8000/stats/ -OutFile stats.json
Get-Content stats.json
```

**Method C: Test from Inside Backend Container**
```powershell
# Execute curl directly in backend container
docker exec web_app_output_jan_2026_float-backend curl -s http://localhost:8000/measure/ | head -c 500

# Or access Python shell to test database manually
docker exec -it web_app_output_jan_2026_float-backend python
# Then in Python:
# from sqlalchemy import create_engine
# from sql_alchemy import Measure
# engine = create_engine('sqlite:///./ai_sandbox_PSA_16_Oct_2025_Cedric_v2.db')
# Session = sessionmaker(bind=engine)
# session = Session()
# print(session.query(Measure).count())  # Should print count of measures
```

### Step 2: Verify Frontend API Calls

Check if the frontend is making the correct API calls and receiving data.

**Method A: Browser Developer Tools (Recommended)**
1. Open the web app: http://localhost:3000
2. Press `F12` to open Developer Tools
3. Go to **Network** tab
4. Look for requests to `/measure/` endpoint
5. Check:
   - **Status**: Should be `200` (success)
   - **Response**: Should be JSON array with measure data
   - **Headers**: Should show `Content-Type: application/json`

**Method B: Check Browser Console for Errors**
1. Open Developer Tools (`F12`)
2. Go to **Console** tab
3. Look for any red error messages
4. Common errors:
   - `Cannot load from /measure/` → Backend not running or endpoint doesn't exist
   - `CORS error` → Frontend/backend origin mismatch
   - `Response is empty` → Backend connected but query returned no data

**Method C: Frontend Component Logs**
In the `Renderer.tsx` and `TableComponent.tsx` files, there are console.log statements showing:
```javascript
console.log("[Chart Data] Found array in property: " + foundKey);
console.error("[Chart Data] Error loading data:", err);
console.error("Error fetching table data:", err);
```

### Step 3: Verify Data Configuration in JSON

Check that your UI components have proper data_binding:

```json
// CORRECT: Chart with data_binding
{
  "type": "line-chart",
  "data_binding": {
    "endpoint": "/measure/"
  },
  ...
}

// INCORRECT: Chart without data_binding (this was your issue)
{
  "type": "line-chart",
  // Missing data_binding!
  ...
}
```

Search for all chart components and ensure they have `data_binding` configured.

---

## Comprehensive Database Connectivity Checklist

Use this checklist to verify everything is working:

- [ ] **Database File Exists**
  ```powershell
  Get-Item -Path "path/to/your/database.db"
  ```

- [ ] **Database Path Matches in Backend Code**
  ```python
  # In backend/main_api.py, line ~26
  SQLALCHEMY_DATABASE_URL = "sqlite:///./YOUR_DB_NAME.db"
  ```

- [ ] **Database is Readable**
  ```powershell
  # Check file permissions
  (Get-Item "path/to/database.db").Attributes
  # Should NOT be "ReadOnly"
  ```

- [ ] **Backend Container is Running**
  ```powershell
  docker ps | grep backend
  # Should show running backend container
  ```

- [ ] **Backend API Responds**
  ```powershell
  Invoke-WebRequest -Uri http://localhost:8000/docs
  # Should return status 200
  ```

- [ ] **Database Connection Works**
  ```powershell
  Invoke-WebRequest -Uri http://localhost:8000/stats/
  # Check response has table counts (e.g., "measure_count": 1590)
  ```

- [ ] **Table Has Data**
  ```powershell
  $response = Invoke-WebRequest -Uri http://localhost:8000/measure/
  ($response.Content | ConvertFrom-Json).Count
  # Should show number of records, not 0
  ```

- [ ] **Frontend Components Have data_binding**
  Check in `frontend/src/data/ui_components.json` that every chart has:
  ```json
  "data_binding": {
    "endpoint": "/measure/"
  }
  ```

- [ ] **Frontend Network Requests Succeed**
  Open browser DevTools → Network → filter for `/measure/` → check Status is 200

---

## Common Issues and Solutions

### Issue 1: "No data available for Measure"
**Possible Causes:**
- ✓ Database path mismatch (FIXED in your case)
- Database file missing or corrupted
- Table is actually empty
- Table name is different than expected
- Foreign key relationships missing

**How to Debug:**
```powershell
# Check if table exists and has data
docker exec web_app_output_jan_2026_float-backend python -c "
from sqlalchemy import create_engine, inspect
engine = create_engine('sqlite:///./ai_sandbox_PSA_16_Oct_2025_Cedric_v2.db')
inspector = inspect(engine)
tables = inspector.get_table_names()
print('Tables:', tables)
print('measure in tables:', 'measure' in tables)
"
```

### Issue 2: Charts Show Empty/No Data
**Possible Causes:**
- ✓ Missing `data_binding` property (FIXED in your case)
- Endpoint returns data but in wrong format
- Frontend can't parse response structure

**How to Debug:**
```powershell
# See what the API actually returns
$response = Invoke-WebRequest -Uri http://localhost:8000/measure/
$data = $response.Content | ConvertFrom-Json
$data | Get-Member  # See structure
$data[0]            # See first record structure
```

### Issue 3: CORS Errors in Browser
**Message**: "Access to XMLHttpRequest blocked by CORS policy"

**Solution**: Already configured in your `main_api.py` (lines 87-92):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue 4: Charts Load But Show Wrong Data
**Possible Cause**: Field names don't match between database and chart configuration

**Debug Steps:**
1. Get actual data structure: `Invoke-WebRequest -Uri http://localhost:8000/measure/`
2. Check what fields exist in response
3. Verify chart configuration uses correct field names for:
   - `label-field`: The label to display (e.g., "metric")
   - `data-field`: The value to plot (e.g., "value")

---

## How to Verify Charts Display Data

After your fixes, verify the charts work:

1. **Restart containers** (already done):
   ```powershell
   docker-compose down
   docker-compose up -d --build
   ```

2. **Open the web app**: http://localhost:3000

3. **Check each chart**:
   - Open Developer Tools (F12)
   - Go to Network tab
   - Look for requests to `http://localhost:8000/measure/`
   - Should see Status 200 with data response

4. **Expected Results**:
   - Table shows rows with value, error, uncertainty, unit, measurand, metric, observation
   - Line Chart shows data points plotted
   - Bar Chart shows bars for each metric
   - Radar Chart shows polygon with all metrics

---

## File Changes Made

### 1. `backend/main_api.py` (Line 26)
```diff
- SQLALCHEMY_DATABASE_URL = "sqlite:///./ai_sandbox_PSA_13_Jan_2026.db"
+ SQLALCHEMY_DATABASE_URL = "sqlite:///./ai_sandbox_PSA_16_Oct_2025_Cedric_v2.db"
```

### 2. `frontend/src/data/ui_components.json` (3 locations)
Added to Line Chart (after line ~112):
```json
"data_binding": {
  "endpoint": "/measure/"
},
```

Added to Bar Chart (after line ~166):
```json
"data_binding": {
  "endpoint": "/measure/"
},
```

Added to Radar Chart (after line ~221):
```json
"data_binding": {
  "endpoint": "/measure/"
},
```

---

## Quick Reference: Docker Commands for Debugging

```powershell
# View all containers
docker ps -a

# View logs
docker logs <container_name>

# Execute command in container
docker exec <container_name> <command>

# Restart containers
docker-compose down
docker-compose up -d --build

# Clean up everything
docker-compose down --volumes
docker-compose up -d --build

# Check network connectivity between containers
docker network ls
docker network inspect <network_name>
```

---

## API Documentation

Your backend auto-generates OpenAPI docs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Use these to explore all available endpoints and test them directly in the browser.

---

## Next Steps

1. ✅ All data should now display correctly
2. Test the charts and table in the browser
3. If issues persist, use the debugging steps above
4. Check backend logs: `docker logs -f web_app_output_jan_2026_float-backend`

Good luck! 🚀
