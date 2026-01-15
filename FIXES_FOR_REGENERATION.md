# Dashboard Fixes - Complete Implementation Guide

This guide explains all the fixes needed when regenerating your BESSER dashboard. Since code is generated, fixes are identified by code patterns to search for rather than line numbers.

---

## Overview of All Fixes

| # | File | Issue | Fix |
|---|------|-------|-----|
| 1 | `backend/main_api.py` | Wrong database filename | Update database path |
| 2 | `frontend/src/data/ui_components.json` | Charts missing data_binding | Add endpoint configuration |
| 3 | `frontend/src/data/ui_components.json` | Chart fields use UUIDs not column names | Use actual column names |
| 4 | `frontend/src/components/Renderer.tsx` | Table requests broken ?detailed=true | Remove query parameter |
| 5 | `frontend/src/components/Renderer.tsx` | Charts request broken ?detailed=true | Remove query parameter |
| 6 | `frontend/src/components/table/TableComponent.tsx` | Table requests broken ?detailed=true | Remove query parameter |
| 7 | `frontend/src/components/Renderer.tsx` | Charts read fields from wrong location | Read from attributes object |

---

## FIX 1: Database Path in Backend

**File**: `backend/main_api.py`

**Why**: Backend connects to wrong/non-existent database file, causing all API endpoints to return empty data.

**Search for this code**:
```python
def init_db():
    SQLALCHEMY_DATABASE_URL = "sqlite:///./ai_sandbox_PSA_13_Jan_2026.db"
```

**Replace with**:
```python
def init_db():
    SQLALCHEMY_DATABASE_URL = "sqlite:///./ai_sandbox_PSA_16_Oct_2025_Cedric_v2.db"
```

**Note**: The exact database filename depends on your setup. Replace with the correct `.db` file in your backend directory.

---

## FIX 2: Add data_binding to Line Chart

**File**: `frontend/src/data/ui_components.json`

**Why**: Charts have no endpoint configured, so they don't know where to fetch data from.

**Search for**:
```json
"type": "line-chart",
"chart": {
  "animate": true,
```

Look for the chart block with `"id": "i1cekk"` (Line Chart).

**Find this section in the chart object**:
```json
"color": "#4CAF50",
"display_order": 0,
"id": "i1cekk",
"name": "Line Chart",
```

**Add before `"display_order"`**:
```json
"data_binding": {
  "endpoint": "/measure/"
},
```

**Result**:
```json
"color": "#4CAF50",
"data_binding": {
  "endpoint": "/measure/"
},
"display_order": 0,
```

---

## FIX 3: Add data_binding to Bar Chart

**File**: `frontend/src/data/ui_components.json`

**Search for**:
```json
"type": "bar-chart",
"chart": {
  "animate": true,
```

Look for the chart block with `"id": "ig71rx"` (Bar Chart).

**Find this section**:
```json
"color": "#3498db",
"display_order": 0,
"id": "ig71rx",
"name": "Bar Chart Title",
```

**Add before `"display_order"`**:
```json
"data_binding": {
  "endpoint": "/measure/"
},
```

---

## FIX 4: Add data_binding to Radar Chart

**File**: `frontend/src/data/ui_components.json`

**Search for**:
```json
"type": "radar-chart",
"chart": {
  "dotSize": 3,
```

Look for the chart block with `"id": "irekdw"` (Radar Chart).

**Find this section**:
```json
"color": "#8884d8",
"display_order": 0,
"id": "irekdw",
"name": "Radar Chart",
```

**Add before `"display_order"`**:
```json
"data_binding": {
  "endpoint": "/measure/"
},
```

---

## FIX 5: Fix Line Chart Field Mapping

**File**: `frontend/src/data/ui_components.json`

**Why**: Charts use UUID field names instead of actual column names, causing only 1 point to be plotted.

**Search for the Line Chart attributes**:
```json
"attributes": {
  "animate": true,
  "chart-color": "#4CAF50",
  "chart-title": "Line Chart",
  "curve-type": "monotone",
  "data-field": "c1748cab-b490-4f3a-831e-0568ca940062",
```

**Replace the UUID fields**:

Find:
```json
"data-field": "c1748cab-b490-4f3a-831e-0568ca940062",
```

Replace with:
```json
"data-field": "value",
```

Find:
```json
"label-field": "c1748cab-b490-4f3a-831e-0568ca940062",
```

Replace with:
```json
"label-field": "metric_id",
```

---

## FIX 6: Fix Bar Chart Field Mapping

**File**: `frontend/src/data/ui_components.json`

**Search for the Bar Chart attributes**:
```json
"attributes": {
  "bar-width": 30,
  "chart-color": "#3498db",
  "chart-title": "Bar Chart Title",
  "data-field": "c1748cab-b490-4f3a-831e-0568ca940062",
```

**Replace**:

Find:
```json
"data-field": "c1748cab-b490-4f3a-831e-0568ca940062",
```

Replace with:
```json
"data-field": "value",
```

Find:
```json
"label-field": "",
```

Replace with:
```json
"label-field": "metric_id",
```

---

## FIX 7: Fix Radar Chart Field Mapping

**File**: `frontend/src/data/ui_components.json`

**Search for the Radar Chart attributes**:
```json
"attributes": {
  "chart-color": "#8884d8",
  "chart-title": "Radar Chart",
  "data-field": "c1748cab-b490-4f3a-831e-0568ca940062",
```

**Replace**:

Find:
```json
"data-field": "c1748cab-b490-4f3a-831e-0568ca940062",
```

Replace with:
```json
"data-field": "value",
```

Find:
```json
"label-field": "c1748cab-b490-4f3a-831e-0568ca940062",
```

Replace with:
```json
"label-field": "metric_id",
```

Also update the series JSON (it's a JSON string, so look for the field name inside):

Find:
```json
"data-field\":\"c1748cab-b490-4f3a-831e-0568ca940062\"
```

Replace with:
```json
"data-field\":\"value\"
```

---

## FIX 8: Remove ?detailed=true from Renderer.tsx

**File**: `frontend/src/components/Renderer.tsx`

**Why**: The `?detailed=true` parameter causes 500 errors due to schema mismatch in the database.

**Search for**:
```tsx
// Check if table has lookup columns - if so, request detailed data with joins
const hasLookupColumns = component.chart?.columns?.some(
  (col: any) => typeof col === 'object' && col.column_type === 'lookup'
);

// Add detailed=true query param if there are lookup columns
const urlParams = hasLookupColumns ? '?detailed=true' : '';
const url = endpoint.startsWith("/") 
  ? backendBase + endpoint + urlParams
  : endpoint + urlParams;
```

**Replace with**:
```tsx
const url = endpoint.startsWith("/") 
  ? backendBase + endpoint
  : endpoint;
```

**Note**: There are TWO places where this code appears - one for charts and one for tables. Find both and apply this fix to both.

To find them, search for:
```tsx
if (["bar-chart", "line-chart", "pie-chart", "radial-bar-chart", "radar-chart", "metric-card", "table"].includes(component.type))
```

Then look for the two occurrences:
1. First one near the top - handles chart data fetching (around line 40-70)
2. Second one in the table fetch - inside table component (around line 80-100)

---

## FIX 9: Remove ?detailed=true from TableComponent.tsx

**File**: `frontend/src/components/table/TableComponent.tsx`

**Search for**:
```tsx
// Check if table has lookup columns - if so, request detailed data with joins
const hasLookupColumns = options?.columns?.some(
  (col: any) => typeof col === 'object' && col.column_type === 'lookup'
);

// Add detailed=true query param if there are lookup columns
const urlParams = hasLookupColumns ? '?detailed=true' : '';
const url = endpoint.startsWith("/") 
  ? backendBase + endpoint + urlParams
  : endpoint + urlParams;
```

**Replace with**:
```tsx
const url = endpoint.startsWith("/") 
  ? backendBase + endpoint
  : endpoint;
```

---

## FIX 10: Fix Chart Field Reading in Renderer.tsx (Line Chart)

**File**: `frontend/src/components/Renderer.tsx`

**Why**: Charts were reading field configuration from wrong object location, so the correct field names weren't being used.

**Search for this in the line-chart section**:
```tsx
if (component.type === "line-chart") {
  if (loading) return <div id={component.id}>Loading data...</div>;
  if (error) return <div id={component.id}>{error}</div>;
  
  // Use configured field names from data_binding, with intelligent fallback
  let actualLabelField = component.data_binding?.label_field || "name";
  let actualDataField = component.data_binding?.data_field || "value";
```

**Replace with**:
```tsx
if (component.type === "line-chart") {
  if (loading) return <div id={component.id}>Loading data...</div>;
  if (error) return <div id={component.id}>{error}</div>;
  
  // Use configured field names from attributes or data_binding
  let actualLabelField = component.attributes?.["label-field"] || 
                        component.data_binding?.label_field || 
                        "name";
  let actualDataField = component.attributes?.["data-field"] || 
                       component.data_binding?.data_field || 
                       "value";
```

---

## FIX 11: Fix Chart Field Reading in Renderer.tsx (Bar Chart)

**File**: `frontend/src/components/Renderer.tsx`

**Search for this in the bar-chart section**:
```tsx
if (component.type === "bar-chart") {
  if (loading) return <div id={component.id}>Loading data...</div>;
  if (error) return <div id={component.id}>{error}</div>;
  
  // Use configured field names from data_binding, with intelligent fallback
  let actualLabelField = component.data_binding?.label_field || "name";
  let actualDataField = component.data_binding?.data_field || "value";
```

**Replace with**:
```tsx
if (component.type === "bar-chart") {
  if (loading) return <div id={component.id}>Loading data...</div>;
  if (error) return <div id={component.id}>{error}</div>;
  
  // Use configured field names from attributes or data_binding
  let actualLabelField = component.attributes?.["label-field"] || 
                        component.data_binding?.label_field || 
                        "name";
  let actualDataField = component.attributes?.["data-field"] || 
                       component.data_binding?.data_field || 
                       "value";
```

---

## FIX 12: Fix Chart Field Reading in Renderer.tsx (Radar Chart)

**File**: `frontend/src/components/Renderer.tsx`

**Search for this in the radar-chart section**:
```tsx
if (component.type === "radar-chart") {
  if (loading) return <div id={component.id}>Loading data...</div>;
  if (error) return <div id={component.id}>{error}</div>;
  
  // Use configured field names from data_binding, with intelligent fallback
  let actualLabelField = component.data_binding?.label_field || "name";
  let actualDataField = component.data_binding?.data_field || "value";
```

**Replace with**:
```tsx
if (component.type === "radar-chart") {
  if (loading) return <div id={component.id}>Loading data...</div>;
  if (error) return <div id={component.id}>{error}</div>;
  
  // Use configured field names from attributes or data_binding
  let actualLabelField = component.attributes?.["label-field"] || 
                        component.data_binding?.label_field || 
                        "name";
  let actualDataField = component.attributes?.["data-field"] || 
                       component.data_binding?.data_field || 
                       "value";
```

---

## Application Order

Apply fixes in this order:

1. **Fix 1** - Database path (backend/main_api.py)
2. **Fix 2-4** - Add data_binding to charts (frontend/src/data/ui_components.json)
3. **Fix 5-7** - Fix chart field mappings (frontend/src/data/ui_components.json)
4. **Fix 8** - Remove ?detailed=true from Renderer.tsx
5. **Fix 9** - Remove ?detailed=true from TableComponent.tsx
6. **Fix 10-12** - Fix chart field reading in Renderer.tsx

---

## Testing After Applying Fixes

1. **Rebuild containers**:
   ```powershell
   docker-compose down
   docker-compose up -d --build
   ```

2. **Test API**:
   ```powershell
   Invoke-WebRequest -Uri http://localhost:8000/measure/ -UseBasicParsing
   # Should return 200 OK with 1500+ JSON records
   ```

3. **Test Frontend**: http://localhost:3000
   - Table should display all rows without "Error loading Data"
   - Line Chart should show multiple data points (not just 1)
   - Bar Chart should show multiple bars (not just 1)
   - Radar Chart should show full polygon (not just 1 point)

4. **Browser Console** (F12 → Console):
   - Should NOT see 500 errors
   - Should see messages like:
     ```
     [Chart Data] Found array in property: 0
     [Line Chart] Using configured fields - labelField: metric_id, dataField: value
     ```

---

## Quick Reference: Code Patterns to Search For

| Fix | Search Pattern |
|-----|----------------|
| 1 | `SQLALCHEMY_DATABASE_URL = "sqlite:///.` |
| 2-4 | `"id": "i1cekk"`, `"id": "ig71rx"`, `"id": "irekdw"` |
| 5-7 | `c1748cab-b490-4f3a-831e-0568ca940062` |
| 8 | `?detailed=true` in chart data fetch |
| 9 | `?detailed=true` in table data fetch |
| 10-12 | `component.data_binding?.label_field` in chart sections |

---

## Why Each Fix is Needed

### Fix 1: Database Path
- **Problem**: Generated code has hardcoded incorrect database filename
- **Impact**: Backend can't connect to database, all data returns empty
- **Solution**: Point to actual database file location

### Fixes 2-4: Add data_binding
- **Problem**: BESSER generates charts without data_binding configuration
- **Impact**: Charts don't know which API endpoint to call for data
- **Solution**: Add endpoint configuration to each chart

### Fixes 5-7: Chart Field Mapping
- **Problem**: BESSER uses UUIDs instead of actual column names for field mapping
- **Impact**: Charts receive data but can't find the correct columns, so only 1 point plots
- **Solution**: Use actual column names from your data (e.g., "value", "metric_id")

### Fix 8: Remove ?detailed=true from Renderer
- **Problem**: Generated code tries to use eager loading with broken schema
- **Impact**: API returns 500 error when detailed=true is requested
- **Solution**: Remove the query parameter - basic endpoint returns all needed data

### Fix 9: Remove ?detailed=true from TableComponent
- **Problem**: Same as Fix 8, but for tables
- **Impact**: Table displays "Error loading Data"
- **Solution**: Remove the query parameter

### Fixes 10-12: Fix Field Reading
- **Problem**: Renderer reads field configuration from data_binding instead of attributes
- **Impact**: Field mappings configured in JSON aren't being used
- **Solution**: Read from attributes first, then fall back to data_binding

---

## Notes for Your Use Case

### For the "measure" Table:
- Database table: `measure`
- API endpoint: `/measure/`
- Key columns:
  - `value` (float) - Y-axis for charts
  - `metric_id` (int) - X-axis label for charts
  - `observation_id` (int) - related observation
  - `unit`, `error`, `uncertainty` - additional fields

### If You Change the Table or Columns:
- Update Fix 1 to point to correct database
- Update Fix 2-4 to use correct endpoint (e.g., `/myentity/`)
- Update Fix 5-7 to use correct column names (e.g., `label-field: "name"`, `data-field: "count"`)

---

## Troubleshooting

**Issue**: Charts still show only 1 point after applying fixes
- **Check**: Did you apply Fixes 10-12? These are critical for field reading.
- **Solution**: Verify Renderer.tsx now reads from `component.attributes` first.

**Issue**: Table shows "Error loading Data"
- **Check**: Did you apply Fix 9?
- **Solution**: Search for `?detailed=true` and remove it from TableComponent.

**Issue**: API returns 500 error
- **Check**: Did you apply Fixes 8-9?
- **Solution**: Remove `?detailed=true` from both files.

**Issue**: Database connection error
- **Check**: Did you apply Fix 1?
- **Solution**: Verify database filename matches your actual `.db` file.

---

## FIX 13: Add Filtering Support (Optional Feature)

**File**: `backend/main_api.py`

**Why**: Enable filtering of data on the backend for better performance and data control.

**Search for the `get_all_measure()` function**:
```python
@app.get("/measure/")
def get_all_measure(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    query = database.query(Measure)
```

**Replace with**:
```python
@app.get("/measure/")
def get_all_measure(detailed: bool = False, metric_id: int = None, database: Session = Depends(get_db)) -> list:
    query = database.query(Measure)
    if metric_id is not None:
        query = query.filter(Measure.metric_id == metric_id)
```

**Then find both `if detailed:` blocks in the same function and ensure they both apply the filter before returning**.

---

## FIX 14: Add Filter Support to Renderer (Frontend)

**File**: `frontend/src/components/Renderer.tsx`

**Why**: Frontend needs to send filter parameters to the backend API when charts have filters configured.

**Search for the chart data fetch logic** (around line 37-76):
```tsx
const url = apiEndpoint + endpoint;
const response = await axios.get<any[]>(url);
```

**Replace with**:
```tsx
const url = apiEndpoint + endpoint;
let fetchUrl = url;

// Add filter parameters if configured
const filters = component.data_binding?.filters;
if (filters && typeof filters === 'object') {
  const queryParams = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== null && value !== undefined) {
      queryParams.append(key, String(value));
    }
  });
  const queryString = queryParams.toString();
  if (queryString) {
    fetchUrl += (fetchUrl.includes('?') ? '&' : '?') + queryString;
  }
}

const response = await axios.get<any[]>(fetchUrl);
```

---

## FIX 15: Add Filter Support to TableComponent (Frontend)

**File**: `frontend/src/components/table/TableComponent.tsx`

**Why**: Tables also need to support the same filtering mechanism as charts.

**Search for the table data fetch logic** (around line 83-110):
```tsx
const url = `${apiEndpoint}${endpoint}`;
const response = await axios.get<any[]>(url);
```

**Replace with**:
```tsx
const url = `${apiEndpoint}${endpoint}`;
let fetchUrl = url;

// Add filter parameters if configured
const filters = component.data_binding?.filters;
if (filters && typeof filters === 'object') {
  const queryParams = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== null && value !== undefined) {
      queryParams.append(key, String(value));
    }
  });
  const queryString = queryParams.toString();
  if (queryString) {
    fetchUrl += (fetchUrl.includes('?') ? '&' : '?') + queryString;
  }
}

const response = await axios.get<any[]>(fetchUrl);
```

---

## FIX 16: Add Filters to Chart Configuration in JSON

**File**: `frontend/src/data/ui_components.json`

**Why**: Configure which filters to apply to each chart when displaying data.

**For Line Chart** - Search for:
```json
"id": "i1cekk",
"data_binding": {
  "endpoint": "/measure/"
}
```

**Replace with**:
```json
"id": "i1cekk",
"data_binding": {
  "endpoint": "/measure/",
  "filters": {
    "metric_id": 1
  }
}
```

**For Bar Chart** - Search for:
```json
"id": "ig71rx",
"data_binding": {
  "endpoint": "/measure/"
}
```

**Replace with**:
```json
"id": "ig71rx",
"data_binding": {
  "endpoint": "/measure/",
  "filters": {
    "metric_id": 1
  }
}
```

**For Radar Chart** - Search for:
```json
"id": "irekdw",
"data_binding": {
  "endpoint": "/measure/"
}
```

**Replace with**:
```json
"id": "irekdw",
"data_binding": {
  "endpoint": "/measure/",
  "filters": {
    "metric_id": 1
  }
}
```

---

## Summary Checklist

- [ ] Fix 1: Database path in main_api.py
- [ ] Fix 2: Add data_binding to Line Chart
- [ ] Fix 3: Add data_binding to Bar Chart
- [ ] Fix 4: Add data_binding to Radar Chart
- [ ] Fix 5: Fix Line Chart field mapping (UUID → value, metric_id)
- [ ] Fix 6: Fix Bar Chart field mapping (UUID → value, metric_id)
- [ ] Fix 7: Fix Radar Chart field mapping (UUID → value, metric_id)
- [ ] Fix 8: Remove ?detailed=true from Renderer.tsx (chart section)
- [ ] Fix 9: Remove ?detailed=true from TableComponent.tsx
- [ ] Fix 10: Fix Line Chart field reading in Renderer.tsx
- [ ] Fix 11: Fix Bar Chart field reading in Renderer.tsx
- [ ] Fix 12: Fix Radar Chart field reading in Renderer.tsx
- [ ] **[Optional]** Fix 13: Add filtering support to backend API
- [ ] **[Optional]** Fix 14: Add filter support to Renderer component
- [ ] **[Optional]** Fix 15: Add filter support to TableComponent
- [ ] **[Optional]** Fix 16: Add filters to chart configuration
- [ ] Rebuild: `docker-compose down && docker-compose up -d --build`
- [ ] Test: Open http://localhost:3000 and verify data displays
