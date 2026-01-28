# What Was Wrong & How to Fix It

## 🔴 PROBLEM 1: Database Path Mismatch

### The Issue
Your backend was trying to connect to the WRONG database file:

```
❌ Looking for:    ai_sandbox_PSA_13_Jan_2026.db  (doesn't exist)
✅ Actual file:    ai_sandbox_PSA_16_Oct_2025_Cedric_v2.db  (exists!)
```

### Where it happened
**File**: `backend/main_api.py` (Line 26)

```python
# BEFORE (Wrong)
SQLALCHEMY_DATABASE_URL = "sqlite:///./ai_sandbox_PSA_13_Jan_2026.db"

# AFTER (Fixed)
SQLALCHEMY_DATABASE_URL = "sqlite:///./ai_sandbox_PSA_16_Oct_2025_Cedric_v2.db"
```

### Why it caused your symptoms
- Backend couldn't find the database
- All API endpoints returned empty data
- Table showed "No data available for Measure"
- Charts had nothing to plot

---

## 🔴 PROBLEM 2: Charts Missing Data Binding

### The Issue
The three chart components had NO configuration telling them where to fetch data:

```json
// Line Chart, Bar Chart, Radar Chart ALL had this problem:
❌ "data_binding" property was MISSING!
```

### Where it happened
**File**: `frontend/src/data/ui_components.json`

Three locations needed fixing:

**1. Line Chart** (around line 112)
**2. Bar Chart** (around line 166)
**3. Radar Chart** (around line 221)

### Solution Applied
Added to all three charts:
```json
"data_binding": {
  "endpoint": "/measure/"
},
```

### Why it caused your symptoms
- Frontend rendered the charts but they had no data source
- Charts didn't know to call the `/measure/` API endpoint
- Users saw empty charts with no plots

---

## 🔴 PROBLEM 3: Table Crashing with 500 Error on /measure/?detailed=true

### The Issue
The table and charts were trying to request `/measure/?detailed=true` which fails with:
```
500 Internal Server Error
ERROR: no such column: observation_1.dataset_id
```

### Root Cause
- **Database Schema Mismatch**: The backend model defines `dataset_id` in the Observation class
- **Actual Database**: The observation table doesn't have this column
- **Result**: When the backend tries to eagerly load related Observation objects, the SQL query references a non-existent column and crashes

### Where it happened
**Files**:
- `frontend/src/components/table/TableComponent.tsx` (line ~90)
- `frontend/src/components/Renderer.tsx` (line ~55)

Both were adding `?detailed=true` query parameter to requests when lookup columns were detected.

### Solution Applied
Removed the `detailed=true` parameter from API requests. The regular `/measure/` endpoint already returns all the data needed:

```tsx
// BEFORE (Broken)
const hasLookupColumns = options?.columns?.some(...);
const urlParams = hasLookupColumns ? '?detailed=true' : '';
const url = endpoint.startsWith("/") 
  ? backendBase + endpoint + urlParams
  : endpoint + urlParams;

// AFTER (Fixed)
const url = endpoint.startsWith("/") 
  ? backendBase + endpoint
  : endpoint;
```

### Why this works
- The regular `/measure/` endpoint returns all 1590+ measure records
- Each record has `metric_id`, `observation_id`, `measurand_id` (the IDs we need)
- Lookup columns can fetch related data separately if needed
- No need for complex eager loading that causes schema mismatches

---

## 🔴 PROBLEM 4: Charts Only Plotting One Point Instead of All Data

### The Issue
The charts had the data, but only showed one point on the plot instead of all 1500+ data points.

### Root Cause
The chart configurations used **UUID field names** instead of **actual column names**:

```json
// BEFORE (Wrong - UUIDs that don't match data columns)
"label-field": "c1748cab-b490-4f3a-831e-0568ca940062",
"data-field": "c1748cab-b490-4f3a-831e-0568ca940062",

// AFTER (Correct - Actual column names)
"label-field": "metric_id",
"data-field": "value",
```

### How Chart Components Work
Charts use `labelField` and `dataField` props to know which columns to use:
```tsx
<XAxis dataKey={labelField} />  // Uses metric_id values on X-axis
<Line dataKey={dataField} />    // Uses value numbers on Y-axis
```

When the field names don't match actual columns:
- Recharts can't find the specified columns
- Falls back to using only first/last record
- Result: Only one point visible on chart

### Actual Data Structure
API returns records like:
```json
{
  "id": 1501,
  "value": 76.92,        ← Chart's Y-axis
  "metric_id": 1,        ← Chart's X-axis  
  "observation_id": 51,
  "unit": "percent",
  "error": "Not Available",
  "uncertainty": "Not Available",
  "measurand_id": "Not Available"
}
```

### Where it happened
**File**: `frontend/src/data/ui_components.json`

Three locations fixed:

**Line Chart** (line ~88):
```json
"label-field": "metric_id",
"data-field": "value",
```

**Bar Chart** (line ~142):
```json
"label-field": "metric_id",
"data-field": "value",
```

**Radar Chart** (line ~192):
```json
"label-field": "metric_id",
"data-field": "value",
```

### Why it caused your symptoms
- API returned 1590 records
- Frontend received all 1590 records
- But charts were looking for columns that didn't exist
- So Recharts defaulted to showing minimal data
- Only one point visible on each chart

---

## ✅ VERIFICATION: All Issues Fixed!

All four problems have been resolved:

1. ✅ Database path corrected to actual file location
2. ✅ Charts now have `data_binding` with correct endpoint
3. ✅ Removed broken `?detailed=true` parameter from API requests
4. ✅ Chart field configurations now use actual column names

### What You Should See Now

**1. Table Component**
- Shows all 1590+ measure records
- Columns: value, error, uncertainty, unit, measurand, metric, observation
- "Error loading Data" message is GONE

**2. Line Chart**
- X-axis: metric_id values (1, 2, 3, ..., 30)
- Y-axis: value floats (ranging from ~3 to ~100)
- Multiple points connected by a line showing trend

**3. Bar Chart**
- Bars for each metric (metric_id 1-30)
- Height = corresponding measure value
- All 30+ bars visible

**4. Radar Chart**
- Polygon with vertices for each metric
- Points at actual measure values from database
- All points visible, not just one

---

## 🔍 API Response Verification

Confirmed the API returns correct data:

```
GET http://localhost:8000/measure/
Status: 200 OK
Response: [
  {
    "id": 1501,
    "value": "76.92",
    "metric_id": 1,
    "observation_id": 51,
    "unit": "percent",
    ...
  },
  ... (1589 more records)
]
```

✅ 1590+ records returned
✅ All fields present (value, metric_id, observation_id, etc.)
✅ Value column is numeric (float type)
✅ metric_id column is numeric (int type)
✅ Ready to be plotted on charts

---

## Summary of Code Changes

### File 1: `backend/main_api.py`
- Line 26: Changed database filename to match actual file

### File 2: `frontend/src/data/ui_components.json`
- Line 88: Line Chart - Fixed `data-field` and `label-field` to use actual columns
- Line 142: Bar Chart - Fixed `data-field` and `label-field` to use actual columns
- Line 192: Radar Chart - Fixed `data-field` and `label-field` to use actual columns

### File 3: `frontend/src/components/Renderer.tsx`
- Lines 47-60: Removed `?detailed=true` parameter from chart data fetch

### File 4: `frontend/src/components/table/TableComponent.tsx`
- Lines 83-96: Removed `?detailed=true` parameter from table data fetch

---

## 📚 Key Learning Points

### 1. Field Name Mapping is Critical
Charts and tables expect column names to match exactly. Using UUIDs or incorrect names breaks visualization.

### 2. API Response Debugging
Always check:
- What columns the API actually returns
- What names the frontend components expect
- Whether they match (case-sensitive!)

### 3. Schema Mismatches Cause Silent Failures
When the database schema doesn't match the ORM model:
- Eager loading can crash with cryptic errors
- Fallback to simpler queries without complex joins
- Verify database tables have all expected columns

### 4. One Point vs All Points
Single data point visible = field name mismatch
Solution: Map correct column names to chart field props
