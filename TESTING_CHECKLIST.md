# ChemViz Frontend Testing Checklist

**Testing Date:** February 4, 2026  
**Frontend URL:** http://localhost:3001  
**Backend URL:** http://127.0.0.1:8000

---

## ✅ Prerequisites

- [x] Django backend running on port 8000
- [x] React frontend running on port 3001
- [ ] Sample CSV file ready: `sample_data/sample_equipment_data.csv`

---

## 1. Authentication Flow Testing

### Test 1.1: User Registration
**Steps:**
1. Open http://localhost:3001
2. You should be redirected to `/dashboard` (then to `/login` if not authenticated)
3. Click "Register here" link
4. Fill in registration form:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `testpass123`
   - Confirm Password: `testpass123`
5. Click "Register" button

**Expected Results:**
- ✅ Form validates all fields
- ✅ Success message appears
- ✅ Auto-login after registration
- ✅ Redirect to dashboard
- ✅ Navbar shows username and logout button

**Status:** [ ] Pass [ ] Fail

---

### Test 1.2: User Login
**Steps:**
1. If logged in, click "Logout" in navbar
2. Navigate to http://localhost:3001/login
3. Enter credentials:
   - Username: `testuser`
   - Password: `testpass123`
4. Click "Login" button

**Expected Results:**
- ✅ Successful login
- ✅ Token stored in localStorage
- ✅ Redirect to dashboard
- ✅ Protected routes accessible

**Status:** [ ] Pass [ ] Fail

---

### Test 1.3: User Logout
**Steps:**
1. While logged in, click "Logout" button in navbar
2. Observe redirect

**Expected Results:**
- ✅ Token removed from localStorage
- ✅ Redirect to login page
- ✅ Protected routes inaccessible
- ✅ Attempting to access `/dashboard` redirects to `/login`

**Status:** [ ] Pass [ ] Fail

---

### Test 1.4: Protected Route Access
**Steps:**
1. Log out completely
2. Try to access http://localhost:3001/dashboard directly
3. Try to access http://localhost:3001/upload directly

**Expected Results:**
- ✅ Immediate redirect to `/login`
- ✅ After login, redirect back to originally requested page

**Status:** [ ] Pass [ ] Fail

---

## 2. CSV Upload Testing

### Test 2.1: Upload via Drag & Drop
**Steps:**
1. Login to application
2. Navigate to http://localhost:3001/upload
3. Drag `sample_equipment_data.csv` onto upload zone
4. Click "Upload CSV" button

**Expected Results:**
- ✅ File name displays in preview
- ✅ Upload progress shown
- ✅ Success message appears
- ✅ Redirect to dashboard with new dataset
- ✅ Dataset appears in history sidebar

**Status:** [ ] Pass [ ] Fail

---

### Test 2.2: Upload via File Browse
**Steps:**
1. Navigate to upload page
2. Click "Browse files" link
3. Select `sample_equipment_data.csv` from file dialog
4. Click "Upload CSV" button

**Expected Results:**
- ✅ File selection works
- ✅ Same results as drag & drop test

**Status:** [ ] Pass [ ] Fail

---

### Test 2.3: Invalid File Upload
**Steps:**
1. Try to upload a .txt or .xlsx file
2. Try to upload CSV with wrong columns

**Expected Results:**
- ✅ File type validation error
- ✅ Column validation error from backend
- ✅ Clear error message displayed

**Status:** [ ] Pass [ ] Fail

---

## 3. Dashboard Data Display Testing

### Test 3.1: Summary Cards
**Steps:**
1. Navigate to dashboard with uploaded dataset
2. Observe summary cards at top

**Expected Results:**
- ✅ Dataset info card shows filename and upload date
- ✅ Total Equipment card shows correct count
- ✅ Average Flowrate card shows correct value (m³/h)
- ✅ Average Pressure card shows correct value (bar)
- ✅ Average Temperature card shows correct value (°C)
- ✅ All cards have distinct green color schemes
- ✅ Custom SVG icons display correctly

**Status:** [ ] Pass [ ] Fail

---

### Test 3.2: Data Table
**Steps:**
1. Scroll to "Equipment Data" section
2. Test table functionality:
   - Click column headers to sort
   - Use search box to filter
   - Navigate pages with Previous/Next

**Expected Results:**
- ✅ All columns display: Equipment Name, Type, Flowrate, Pressure, Temperature
- ✅ Sorting works (ascending/descending)
- ✅ Sort arrows update correctly
- ✅ Search filters across all columns
- ✅ Pagination shows 10 rows per page
- ✅ "Showing X of Y equipments" count is accurate
- ✅ Forest green headers with sage green alternating rows
- ✅ Numeric values right-aligned

**Status:** [ ] Pass [ ] Fail

---

## 4. Chart Testing

### Test 4.1: Type Distribution Chart (Doughnut)
**Steps:**
1. Locate "Equipment Type Distribution" chart
2. Hover over chart segments
3. Check legend

**Expected Results:**
- ✅ Doughnut chart renders correctly
- ✅ All equipment types shown
- ✅ Tooltips show count and percentage
- ✅ Legend displays at bottom
- ✅ Green color palette used
- ✅ Summary shows "Total Types" and "Total Equipment"

**Status:** [ ] Pass [ ] Fail

---

### Test 4.2: Parameter Bar Chart
**Steps:**
1. Locate "Average Parameters" chart
2. Hover over bars

**Expected Results:**
- ✅ Three bars: Flowrate, Pressure, Temperature
- ✅ Bar heights proportional to values
- ✅ Tooltips show exact values
- ✅ Y-axis scales appropriately
- ✅ Green gradient bars with rounded corners
- ✅ Summary shows all three averages with units

**Status:** [ ] Pass [ ] Fail

---

### Test 4.3: Parameter Comparison Chart (Line)
**Steps:**
1. Locate "Parameter Comparison" chart
2. Use dropdown to change parameter (Flowrate/Pressure/Temperature)
3. Use type filter to select equipment type
4. Hover over data points

**Expected Results:**
- ✅ Line chart renders with smooth curve
- ✅ Parameter dropdown changes chart data
- ✅ Type filter updates visible equipment
- ✅ Tooltips show equipment name and value
- ✅ X-axis shows equipment names (rotated labels)
- ✅ Forest green line with fill

**Status:** [ ] Pass [ ] Fail

---

## 5. Dataset History Testing

### Test 5.1: History Sidebar (Desktop)
**Steps:**
1. View dashboard on desktop (>768px width)
2. Observe right sidebar
3. Upload multiple datasets (up to 5)

**Expected Results:**
- ✅ Sidebar always visible
- ✅ Shows last 5 datasets
- ✅ Each item shows: name, date, record count
- ✅ Active dataset highlighted
- ✅ Click on dataset loads it in dashboard
- ✅ Refresh button works
- ✅ "Showing last 5 datasets" note appears when 5 datasets exist

**Status:** [ ] Pass [ ] Fail

---

### Test 5.2: History Sidebar (Mobile)
**Steps:**
1. Resize browser to <768px width
2. Look for floating "History" button (bottom-right)
3. Click button to open sidebar
4. Select a dataset
5. Click outside overlay to close

**Expected Results:**
- ✅ Floating button appears on mobile
- ✅ Sidebar slides in from right
- ✅ Overlay darkens background
- ✅ Sidebar auto-closes after selection
- ✅ Close button (X) works
- ✅ Click overlay closes sidebar

**Status:** [ ] Pass [ ] Fail

---

### Test 5.3: Delete Dataset (Optional)
**Steps:**
1. Hover over history item
2. Click delete button (trash icon)
3. Confirm deletion

**Expected Results:**
- ✅ Delete button appears on hover (desktop)
- ✅ Delete button always visible (mobile)
- ✅ Confirmation dialog appears
- ✅ Dataset removed from list
- ✅ If active dataset deleted, dashboard updates
- ✅ Next dataset auto-selected

**Status:** [ ] Pass [ ] Fail

---

## 6. PDF Download Testing

### Test 6.1: Generate PDF Report
**Steps:**
1. Navigate to dashboard with dataset
2. Click "Download PDF" button
3. Wait for generation
4. Open downloaded PDF

**Expected Results:**
- ✅ Button shows loading state (spinner + "Generating...")
- ✅ PDF downloads automatically
- ✅ Filename format: `[dataset_name]_report.pdf`
- ✅ PDF contains:
  - Header with title and date
  - Summary statistics
  - Type distribution table
  - Equipment data table
- ✅ No errors in console

**Status:** [ ] Pass [ ] Fail

---

### Test 6.2: PDF Download Error Handling
**Steps:**
1. Stop Django backend
2. Try to download PDF
3. Restart backend

**Expected Results:**
- ✅ Error alert appears
- ✅ Button returns to normal state
- ✅ User can retry after backend restart

**Status:** [ ] Pass [ ] Fail

---

## 7. Responsive Design Testing

### Test 7.1: Desktop View (≥1024px)
**Steps:**
1. Set browser width to 1440px
2. Navigate through all pages

**Expected Results:**
- ✅ Dashboard: Sidebar + main content layout
- ✅ Summary cards: 4-5 cards per row
- ✅ Charts: 2 columns (Type + Bar), full width (Line)
- ✅ Table: All columns visible
- ✅ Upload page: Centered with comfortable width
- ✅ Auth pages: Centered cards

**Status:** [ ] Pass [ ] Fail

---

### Test 7.2: Tablet View (768px - 1023px)
**Steps:**
1. Set browser width to 800px
2. Test all pages

**Expected Results:**
- ✅ Summary cards: 3-4 cards per row
- ✅ Charts: Stacked (1 column)
- ✅ Table: Horizontal scroll if needed
- ✅ Sidebar: Still visible but narrower
- ✅ Buttons and controls adapt

**Status:** [ ] Pass [ ] Fail

---

### Test 7.3: Mobile View (≤767px)
**Steps:**
1. Set browser width to 375px (iPhone SE)
2. Test all pages

**Expected Results:**
- ✅ Navbar: Stacked or hamburger menu
- ✅ Summary cards: 2 columns, then 1 column
- ✅ Charts: Full width, stacked
- ✅ Table: Horizontal scroll, compact padding
- ✅ Upload: Full width with touch-friendly drag zone
- ✅ History: Floating button with slide-in sidebar
- ✅ Buttons: Full width where appropriate

**Status:** [ ] Pass [ ] Fail

---

### Test 7.4: Touch Interactions (Mobile/Tablet)
**Steps:**
1. Use browser's device emulation
2. Test touch interactions:
   - Tap buttons
   - Swipe to scroll
   - Pinch to zoom
   - Drag files to upload

**Expected Results:**
- ✅ All tap targets ≥44px
- ✅ No hover-only interactions
- ✅ Smooth scrolling
- ✅ Touch gestures work

**Status:** [ ] Pass [ ] Fail

---

## 8. Navigation Testing

### Test 8.1: Navbar Links
**Steps:**
1. Click each navbar link:
   - ChemViz logo/brand
   - Dashboard
   - Upload

**Expected Results:**
- ✅ Brand click navigates to `/dashboard`
- ✅ Dashboard link navigates to `/dashboard`
- ✅ Upload link navigates to `/upload`
- ✅ Active link underlined
- ✅ Hover animations work

**Status:** [ ] Pass [ ] Fail

---

### Test 8.2: Direct URL Navigation
**Steps:**
1. Navigate to URLs directly:
   - http://localhost:3001/
   - http://localhost:3001/dashboard
   - http://localhost:3001/dataset/1
   - http://localhost:3001/upload
   - http://localhost:3001/invalid-route

**Expected Results:**
- ✅ `/` redirects to `/dashboard`
- ✅ `/dashboard` loads dashboard
- ✅ `/dataset/:id` loads specific dataset
- ✅ `/upload` loads upload page
- ✅ Invalid routes redirect to `/dashboard`
- ✅ All protected routes require authentication

**Status:** [ ] Pass [ ] Fail

---

## 9. Error Handling Testing

### Test 9.1: Network Errors
**Steps:**
1. Stop Django backend
2. Try to:
   - Login
   - Upload file
   - Load dashboard
   - Download PDF

**Expected Results:**
- ✅ User-friendly error messages
- ✅ No app crashes
- ✅ Console shows network errors (expected)
- ✅ Retry mechanisms work when backend restarts

**Status:** [ ] Pass [ ] Fail

---

### Test 9.2: Empty States
**Steps:**
1. Fresh user with no datasets
2. Navigate to dashboard

**Expected Results:**
- ✅ "No Data Available" message displays
- ✅ Chemistry flask illustration shows
- ✅ "Upload Dataset" button prominent
- ✅ No JavaScript errors

**Status:** [ ] Pass [ ] Fail

---

### Test 9.3: Loading States
**Steps:**
1. Observe loading states during:
   - Login
   - Data fetch
   - File upload
   - PDF generation

**Expected Results:**
- ✅ Spinner animations display
- ✅ Loading text shows
- ✅ Buttons disabled during loading
- ✅ No content flash/flicker

**Status:** [ ] Pass [ ] Fail

---

## 10. Performance Testing

### Test 10.1: Large Dataset
**Steps:**
1. Upload CSV with 100+ rows
2. Observe rendering time

**Expected Results:**
- ✅ Table paginates correctly
- ✅ Charts render without lag
- ✅ Search/filter remains responsive
- ✅ No browser freezing

**Status:** [ ] Pass [ ] Fail

---

### Test 10.2: Multiple Dataset Switching
**Steps:**
1. Upload 5 different datasets
2. Rapidly switch between them in history

**Expected Results:**
- ✅ Smooth transitions
- ✅ Data updates correctly
- ✅ No stale data displayed
- ✅ Charts re-render properly

**Status:** [ ] Pass [ ] Fail

---

## 11. Browser Compatibility

### Test 11.1: Chrome/Edge (Chromium)
**Status:** [ ] Pass [ ] Fail

### Test 11.2: Firefox
**Status:** [ ] Pass [ ] Fail

### Test 11.3: Safari (if available)
**Status:** [ ] Pass [ ] Fail

---

## 12. Accessibility Testing

### Test 12.1: Keyboard Navigation
**Steps:**
1. Use Tab key to navigate
2. Use Enter/Space to activate buttons
3. Use arrow keys in dropdowns

**Expected Results:**
- ✅ All interactive elements focusable
- ✅ Focus indicators visible
- ✅ Logical tab order
- ✅ No keyboard traps

**Status:** [ ] Pass [ ] Fail

---

### Test 12.2: Screen Reader (Optional)
**Steps:**
1. Use browser's screen reader
2. Navigate through pages

**Expected Results:**
- ✅ Alt text on SVG icons
- ✅ Labels on form inputs
- ✅ ARIA attributes where needed

**Status:** [ ] Pass [ ] Fail

---

## Test Summary

**Total Tests:** 35  
**Passed:** ___  
**Failed:** ___  
**Pass Rate:** ___%

---

## Issues Found

| Issue # | Description | Severity | Status |
|---------|-------------|----------|--------|
| 1 | | High/Medium/Low | Open/Fixed |
| 2 | | High/Medium/Low | Open/Fixed |
| 3 | | High/Medium/Low | Open/Fixed |

---

## Notes & Observations

- 
- 
- 

---

## Next Steps

1. [ ] Fix all High severity issues
2. [ ] Document known limitations
3. [ ] Prepare for deployment testing
4. [ ] Update README with screenshots
5. [ ] Record demo video

---

**Tested By:** ___________  
**Date Completed:** ___________  
**Sign-off:** ___________
