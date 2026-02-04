# UI Redesign Testing Checklist

## Before Proceeding to Step 3.4

Please test the redesigned UI to ensure everything works as expected.

## Setup

### 1. Start Django Backend (if not running)
```powershell
cd C:\Users\AARYA\Desktop\FOSSEE\backend
.\venv\Scripts\python.exe manage.py runserver
```
Expected: Server running at http://127.0.0.1:8000

### 2. Start React Dev Server (if not running)
```powershell
cd C:\Users\AARYA\Desktop\FOSSEE\frontend-web
npm start
```
Expected: Opens http://localhost:3000 automatically

## Visual Testing Checklist

### ✓ Global Styles (App.css)

- [ ] Page background is soft sage green (#E6F0EB)
- [ ] Headings use Georgia serif font
- [ ] Body text uses Inter sans-serif font
- [ ] Buttons have forest green color (#2F5C46)
- [ ] Cards have white background with subtle shadow
- [ ] Smooth transitions on hover (0.3s ease)

**How to Test:** Open any page and inspect typography and colors

---

### ✓ Login/Register Pages

- [ ] Pages still work (not broken by global CSS changes)
- [ ] Forms are readable and functional
- [ ] Buttons respond to clicks
- [ ] Error messages display correctly
- [ ] Navigation between login/register works

**How to Test:**
1. Go to http://localhost:3000/login
2. Try logging in with test credentials
3. Click "Create an account" to go to register
4. Verify both pages load without errors

---

### ✓ Navbar (Layout Component)

- [ ] Navbar appears at top of page after login
- [ ] Flask icon (⚗️) displays next to "ChemViz" brand name
- [ ] Brand name uses serif font (Georgia)
- [ ] "Dashboard" and "Upload" navigation links visible
- [ ] Username displays on the right
- [ ] Logout button present and styled correctly
- [ ] Navbar is sticky (stays at top when scrolling)
- [ ] Hover effects work on navigation links (underline animation)
- [ ] Click on brand/flask navigates to dashboard

**How to Test:**
1. Log in successfully
2. Inspect navbar at top
3. Hover over navigation links
4. Click links to navigate
5. Check that navbar stays visible when scrolling (if content is long)

---

### ✓ Dashboard Page

- [ ] White card displays in center
- [ ] "Dashboard" heading uses serif font
- [ ] Welcome message displays
- [ ] Chemistry flask illustration (SVG) renders correctly
- [ ] Flask has circle background with sage color
- [ ] "Upload Equipment Data" button is forest green
- [ ] Button lifts up on hover (2px)
- [ ] Clicking button navigates to /upload

**How to Test:**
1. Navigate to dashboard after login
2. Inspect card styling and SVG illustration
3. Hover over upload button
4. Click button to go to upload page

---

### ✓ Upload Page - Drop Zone

- [ ] White card with rounded corners displays
- [ ] "Upload Equipment Data" title uses serif font
- [ ] Subtitle text is readable
- [ ] Large dashed-border drop zone visible (350px min height)
- [ ] **Chemistry Flask SVG** displays in center (120x120px)
  - [ ] Flask body (conical shape) renders
  - [ ] Flask neck (horizontal line at top) renders
  - [ ] Liquid inside flask (green, semi-transparent) visible
  - [ ] Three bubbles (circles) display inside liquid
  - [ ] Upload arrow (↑) overlays the flask
- [ ] "Drag & Drop CSV File" title displays
- [ ] "or click to browse your files" subtitle displays
- [ ] Drop zone background is light gray (#F9FAFB)

**How to Test:**
1. Navigate to /upload
2. Inspect the SVG flask illustration carefully
3. Right-click SVG and "Inspect Element" to verify it's inline (not an <img>)

---

### ✓ Upload Page - Hover States

- [ ] Hovering over drop zone changes border to forest green
- [ ] Hovering changes background to sage green
- [ ] Drop zone lifts up 2px on hover
- [ ] Flask icon scales up slightly (1.05x)

**How to Test:** Move mouse over drop zone (don't click yet)

---

### ✓ Upload Page - Drag & Drop

- [ ] Drag a CSV file over the drop zone
- [ ] Border becomes solid forest green (not dashed)
- [ ] Background becomes sage green
- [ ] Glow effect appears (green shadow)
- [ ] Flask icon **bounces up and down** (animation)
- [ ] Text changes to "Drop it here!" and "Release to upload your CSV"
- [ ] Releasing file outside drop zone cancels operation

**How to Test:**
1. Open file explorer
2. Find a CSV file (sample_equipment_data.csv)
3. Drag it over the drop zone (don't drop yet)
4. Observe animations
5. Release file in drop zone

---

### ✓ Upload Page - File Selected

- [ ] After selecting file, drop zone border turns green (success color)
- [ ] File preview card appears below drop zone
- [ ] **Custom CSV Document SVG icon** displays (not emoji 📄)
  - [ ] Document shape with folded corner
  - [ ] "CSV" text inside document
  - [ ] Sage green fill, forest green stroke
- [ ] File name displays correctly
- [ ] File size shows in KB
- [ ] **X button** (SVG cross, not emoji ✕) appears on right
- [ ] Card background is sage green with forest green border
- [ ] Card slides in from top (animation)

**How to Test:**
1. Click drop zone or drag/drop a file
2. Inspect the CSV icon SVG
3. Verify file information is accurate

---

### ✓ Upload Page - Remove File

- [ ] Clicking X button removes the file
- [ ] File preview card disappears
- [ ] Drop zone returns to default state
- [ ] X button rotates 90 degrees on hover
- [ ] X button turns red on hover

**How to Test:**
1. Select a file
2. Hover over X button
3. Click X button
4. Verify file is removed

---

### ✓ Upload Page - Progress Bar

- [ ] Click "Upload & Analyze Data" button
- [ ] Progress section appears below file preview
- [ ] "Analyzing Data" label displays on left
- [ ] Percentage displays on right (serif font)
- [ ] Progress bar is gray background with forest green fill
- [ ] **Liquid wave effect** animates across the fill (white shine)
- [ ] Percentage counts up (0% → 90% → 100%)
- [ ] Bar fills smoothly (width transition)
- [ ] Button changes to "Processing..." with spinner

**How to Test:**
1. Select a valid CSV file
2. Click upload button
3. Watch progress animation
4. Observe liquid wave effect (moving shine)

---

### ✓ Upload Page - Success Message

- [ ] After upload completes, success message appears
- [ ] Message has green background (#D1FAE5)
- [ ] Left border is darker green (accent)
- [ ] Text shows record count: "Success! Uploaded X records. Redirecting..."
- [ ] Message slides down from top (animation)
- [ ] After 2 seconds, automatically redirects to dataset detail page

**How to Test:**
1. Upload sample_equipment_data.csv
2. Wait for success message
3. Verify record count matches CSV (should be 17 for sample file)
4. Wait for auto-redirect

---

### ✓ Upload Page - Error Message

- [ ] If file is invalid (wrong type, too large, empty), error message appears
- [ ] Message has red background (#FEE2E2)
- [ ] Left border is red
- [ ] Error text is descriptive
- [ ] Message slides down from top

**How to Test:**
1. Try to upload a .txt file (should reject)
2. Try to upload a 0-byte file (should reject)
3. Verify error messages are clear

---

### ✓ Upload Page - Requirements Section

- [ ] "File Requirements" heading displays with inline clock SVG icon
- [ ] Heading uses serif font
- [ ] Section has sage green background
- [ ] Left border is forest green (4px)
- [ ] Each requirement has **flask emoji** bullet (⚗️)
- [ ] Requirements listed:
  - Format: CSV files only
  - Size Limit: Maximum 10 MB
  - Row Limit: Up to 10,000 records
  - Required Columns: Equipment Name, Type, Flowrate, Pressure, Temperature
- [ ] Text is readable (charcoal color)
- [ ] "Format", "Size Limit", etc. are bold and forest green

**How to Test:** Scroll down to bottom of upload card

---

### ✓ Upload Page - Animations

- [ ] **Liquid Wave:** Liquid inside flask morphs gently (d-path animation)
- [ ] **Bubbles:** Three bubbles float up and down (different timing)
- [ ] **Upload Arrow:** Arrow pulses (opacity + translateY)
- [ ] **Flask Bounce:** Flask bounces when dragging over drop zone
- [ ] **Progress Liquid:** Shine effect flows across progress bar

**How to Test:**
1. Watch flask for 3-5 seconds (liquid and bubbles animate)
2. Drag file over drop zone (flask bounces)
3. Upload file (progress bar shines)

---

### ✓ Responsive Design - Tablet (768px)

- [ ] Navbar stacks vertically or adjusts layout
- [ ] Flask icon shrinks to 100px
- [ ] Drop zone maintains usability
- [ ] Cards adjust padding
- [ ] Text remains readable

**How to Test:**
1. Open browser DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Set width to 768px
4. Navigate through pages

---

### ✓ Responsive Design - Mobile (480px)

- [ ] Navbar fully responsive (links stack)
- [ ] Flask icon shrinks to 80px
- [ ] Drop zone reduces to 250px min-height
- [ ] File preview card becomes vertical layout
- [ ] Buttons are full width
- [ ] Text is still readable
- [ ] All interactions work on touch

**How to Test:**
1. Set device width to 375px (iPhone size)
2. Test all interactions
3. Verify nothing is cut off

---

### ✓ Dataset Detail Page (Placeholder)

- [ ] After successful upload, redirects to /dataset/:id
- [ ] Placeholder card displays
- [ ] "Dataset Details" heading uses serif font
- [ ] "Upload Another File" button works
- [ ] Layout component wraps the page (navbar visible)

**How to Test:**
1. Complete a file upload
2. Wait for redirect
3. Inspect placeholder page

---

## Known Issues to Ignore

These will be fixed in later steps:

- Dashboard doesn't show actual data yet (placeholder)
- Dataset detail page is empty (Step 3.4-3.7 will build visualization)
- No data table yet (Step 3.4)
- No charts yet (Step 3.5)
- No summary cards yet (Step 3.6)
- No history list yet (Step 3.7)

## Common Problems & Solutions

### Problem: Flask SVG doesn't render
**Solution:** Check browser console for errors. Ensure FileUpload.jsx imported correctly.

### Problem: Colors look wrong
**Solution:** Hard refresh (Ctrl+Shift+R) to clear cached CSS

### Problem: Animations don't work
**Solution:** Check FileUpload.css loaded. Inspect element to verify class names.

### Problem: Navbar missing after login
**Solution:** Verify Layout component imported in App.js. Check AuthContext.

### Problem: Font looks wrong
**Solution:** Georgia is a system font. If not available, serif fallback should work.

### Problem: Progress bar doesn't animate
**Solution:** Check uploadProgress state updates. Inspect progress-bar-fill width style.

## Browser Compatibility

Test in at least one of:
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if on Mac)

All CSS features used (CSS variables, keyframes, flexbox) are widely supported.

## Performance Check

- [ ] Page loads quickly (< 2 seconds)
- [ ] Animations are smooth (60fps)
- [ ] No console errors
- [ ] No console warnings (except React DevTools if present)
- [ ] File upload completes successfully
- [ ] No memory leaks (check DevTools Memory tab if concerned)

## Accessibility Quick Check

- [ ] Tab key navigates through interactive elements
- [ ] Focus states visible (outline on buttons/links)
- [ ] Screen reader can read headings (use NVDA/JAWS if available)
- [ ] Color contrast is sufficient (use Lighthouse audit)
- [ ] SVGs have proper roles (decorative vs informative)

## Final Approval

Once all checkboxes are complete:

**If Everything Looks Good:**
→ Reply "Looks great! Let's proceed with Step 3.4 (DataTable component)"

**If Issues Found:**
→ Reply with specific issues (e.g., "Flask SVG not rendering", "Colors don't match")
→ I'll fix them before moving to Step 3.4

---

## Screenshots to Take (Optional)

If you want to document the new design:

1. Dashboard placeholder page
2. Upload page - empty drop zone with flask
3. Upload page - file selected
4. Upload page - progress bar animating
5. Upload page - success message
6. Mobile view (375px width)

Save these for your final documentation/demo video!

---

## Next Step After Approval

**Step 3.4: Create DataTable Component**

Will include:
- Sortable columns (forest green headers)
- Pagination (10 rows per page)
- Alternating sage green rows
- Custom sort arrow SVGs
- Search/filter functionality (optional)
- Responsive table design
- Same design system as upload component

---

**Design Ready for Production Use** ✓
