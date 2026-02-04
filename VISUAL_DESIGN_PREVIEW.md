# ChemViz UI - Visual Design Preview

## Color Palette

### Primary Colors
```
Sage Green:   ███████ #E6F0EB (Soft, calming background)
Forest Green: ███████ #2F5C46 (Primary actions, emphasis)
White:        ███████ #FFFFFF (Cards, clean surfaces)
Charcoal:     ███████ #1F2937 (Body text, readable)
```

### Semantic Colors
```
Success:      ███████ #10B981 (Upload success, confirmations)
Error:        ███████ #EF4444 (Validation errors, failures)
Warning:      ███████ #F59E0B (Warnings, caution messages)
Info:         ███████ #3B82F6 (Informational messages)
```

## Typography Examples

### Headings (Georgia Serif)
```
H1: Chemical Equipment Parameter Visualizer
H2: Upload Equipment Data
H3: File Requirements
H4: Analyzing Data
```

### Body Text (Inter Sans-serif)
```
Upload your CSV file containing chemical equipment parameters.
Required columns: Equipment Name, Type, Flowrate, Pressure, Temperature.
```

## Component Layouts

### 1. Navbar (Layout.jsx)
```
┌─────────────────────────────────────────────────────────────────┐
│ [Flask] ChemViz     Dashboard  Upload      John Doe  [Logout]  │
└─────────────────────────────────────────────────────────────────┘
```
- White background
- Forest green flask icon and brand name
- Navigation links with underline animation on hover
- User section on right

### 2. File Upload Component (FileUpload.jsx)
```
┌───────────────────────────────────────────────────────────────┐
│  Upload Equipment Data                                        │
│  Upload your CSV file containing chemical equipment parameters│
│                                                               │
│  ╔═══════════════════════════════════════════════════════╗  │
│  ║                                                         ║  │
│  ║                    ⚗️                                   ║  │
│  ║                   ╱  ╲                                  ║  │
│  ║                  ╱    ╲                                 ║  │
│  ║                 ╱  💧  ╲                                ║  │
│  ║                ╱  ○ ○  ╲                               ║  │
│  ║               ╱__________╲                              ║  │
│  ║                    ↑                                    ║  │
│  ║                                                         ║  │
│  ║          Drag & Drop CSV File                           ║  │
│  ║          or click to browse your files                  ║  │
│  ╚═══════════════════════════════════════════════════════╝  │
│                                                               │
│  File Requirements                                            │
│  ⚗️ Format: CSV files only                                    │
│  ⚗️ Size Limit: Maximum 10 MB                                 │
│  ⚗️ Row Limit: Up to 10,000 records                           │
│  ⚗️ Required Columns: Equipment Name, Type, ...               │
│                                                               │
│            [Upload & Analyze Data]                            │
└───────────────────────────────────────────────────────────────┘
```

### 3. File Selected State
```
┌───────────────────────────────────────────────────────────────┐
│  [CSV icon] equipment_data.csv    245.67 KB          [×]     │
└───────────────────────────────────────────────────────────────┘
```
- Sage green background
- Forest green border
- Custom SVG CSV document icon
- X button with rotate animation on hover

### 4. Upload Progress
```
┌───────────────────────────────────────────────────────────────┐
│  Analyzing Data                                          67%  │
│  ████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
└───────────────────────────────────────────────────────────────┘
```
- Forest green gradient fill
- Animated liquid wave effect inside bar
- Percentage in serif font

### 5. Success Message
```
┌───────────────────────────────────────────────────────────────┐
│ ✓ Success! Uploaded 128 records. Redirecting...              │
└───────────────────────────────────────────────────────────────┘
```
- Green background (#D1FAE5)
- Left border accent
- Slide-down animation

### 6. Dashboard Placeholder
```
┌───────────────────────────────────────────────────────────────┐
│                        Dashboard                              │
│   Welcome to ChemViz! Upload your equipment data to start.   │
│                                                               │
│                          ⚗️                                   │
│                         ╱  ╲                                  │
│                        ╱ ○○ ╲                                 │
│                       ╱______╲                                │
│                                                               │
│              [Upload Equipment Data]                          │
└───────────────────────────────────────────────────────────────┘
```

## SVG Illustrations

### Flask Icon (Main Upload Illustration)
```xml
<svg width="120" height="120">
  <path d="M45 15 L45 40 L30 75 ..." /> <!-- Flask body -->
  <line x1="45" y1="15" x2="75" y2="15" /> <!-- Flask neck -->
  <path d="M35 70 Q60 65 85 70 ..." /> <!-- Liquid -->
  <circle cx="45" cy="70" r="3" /> <!-- Bubble 1 -->
  <circle cx="60" cy="75" r="2" /> <!-- Bubble 2 -->
  <circle cx="70" cy="68" r="2.5" /> <!-- Bubble 3 -->
  <path d="M60 50 L60 30 M50 40 L60 30 L70 40" /> <!-- Arrow -->
</svg>
```

### CSV Document Icon
```xml
<svg width="40" height="40">
  <path d="M10 5 L25 5 L30 10 L30 35 L10 35 Z" /> <!-- Document -->
  <path d="M25 5 L25 10 L30 10" /> <!-- Folded corner -->
  <text x="20" y="25">CSV</text> <!-- Label -->
</svg>
```

### Brand Flask Icon (Navbar)
```xml
<svg width="32" height="32">
  <path d="M12 3V10L6 22 ..." /> <!-- Simplified flask -->
  <circle cx="10" cy="18" r="1.5" /> <!-- Bubbles -->
  <circle cx="15" cy="20" r="1" />
  <circle cx="20" cy="17" r="1.5" />
</svg>
```

## Animations

### 1. Hover States
- **Buttons:** Lift up 2px + shadow increase
- **Cards:** Shadow lg → xl
- **Flask Icon:** Scale 1.05
- **Nav Links:** Underline animates from center

### 2. Drag & Drop
- **Border:** Dashed → Solid
- **Background:** White → Sage
- **Flask:** Bounces up and down
- **Shadow:** Glowing forest green

### 3. Progress Bar
- **Fill:** Slides left to right (width transition)
- **Liquid:** Shine effect flows across (transform translateX)
- **Text:** Percentage updates (React state)

### 4. Bubbles
- **Movement:** Float up and down (translateY)
- **Opacity:** Pulsates 0.4 → 0.6
- **Timing:** Staggered delays (0s, 1s, 2s)

### 5. Messages
- **Entrance:** Slide down from top (translateY)
- **Colors:** Background + border match type (success/error/info)

## Button Styles

### Primary Button
```
Background: Forest Green (#2F5C46)
Text: White
Border: 2px solid Forest Green
Hover: Darker green + lift + shadow
Disabled: 50% opacity
```

### Secondary Button
```
Background: White
Text: Forest Green
Border: 2px solid Forest Green
Hover: Sage Green background
```

### Ghost Button
```
Background: Transparent
Text: Forest Green
Border: Transparent
Hover: Sage Green background
```

## Spacing System

```
Component Padding:
- Cards: 32px (--space-xl)
- Drop Zone: 48px (--space-2xl)
- Navbar: 16px vertical, 32px horizontal

Gaps Between Elements:
- Card sections: 24px (--space-lg)
- Form groups: 24px (--space-lg)
- Button + text: 12px (--space-sm)
- Icon + text: 8px (--space-xs)
```

## Responsive Breakpoints

### Tablet (768px and below)
- Font size: 14px base
- Container padding: 16px
- Flask icon: 100px
- Card padding: 24px

### Mobile (480px and below)
- Container padding: 12px
- Flask icon: 80px
- Card padding: 16px
- File preview: Vertical layout
- Drop zone: 250px min-height

## Accessibility Features

1. **Semantic HTML:** Proper heading hierarchy (h1 → h2 → h3)
2. **ARIA Labels:** File input, remove buttons
3. **Focus States:** Visible outlines on keyboard navigation
4. **Color Contrast:** All text meets WCAG AA standards
5. **Alt Text:** SVG elements have titles/descriptions
6. **Keyboard Navigation:** All interactive elements accessible

## Brand Identity

### Name: ChemViz
- **Chem:** Chemistry, Chemical Engineering
- **Viz:** Visualization, Visual Analytics

### Visual Language
- Laboratory equipment (flasks, beakers)
- Chemical reactions (bubbles, liquids)
- Data visualization (charts, tables - coming in 3.4-3.7)
- Professional, scientific, trustworthy

### Voice & Tone
- **Professional:** Clear, precise language
- **Educational:** Helpful requirements and messages
- **Encouraging:** Positive feedback on success
- **Technical:** Appropriate for engineers/scientists

---

## Preview URLs (After Starting Dev Server)

- **Login:** http://localhost:3000/login
- **Register:** http://localhost:3000/register
- **Dashboard:** http://localhost:3000/dashboard (protected)
- **Upload:** http://localhost:3000/upload (protected)

## Files to Test

1. App.css - Global styles load
2. Layout.jsx - Navbar appears on protected pages
3. FileUpload.jsx - Flask illustration renders
4. FileUpload.css - Animations work smoothly
5. UploadPage.jsx - Layout wraps correctly
6. App.js - Routing works with new components

---

**Design Philosophy:** "Clean lab surfaces, precise measurements, trusted results."
