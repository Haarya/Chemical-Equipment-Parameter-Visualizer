"""
ChemViz Pro - Modern Lab OS Stylesheet
A comprehensive QSS theme for a professional laboratory application look
Supports Light and Dark themes
"""

# Light Theme Color Palette
LIGHT_COLORS = {
    'background': '#E6F0EB',      # Soft Sage Green
    'surface': '#FFFFFF',          # Pure White
    'primary': '#2F5C46',          # Deep Forest Green
    'primary_hover': '#3D7A5C',    # Lighter Forest Green
    'primary_pressed': '#1F3D2E',  # Darker Forest Green
    'text': '#374151',             # Charcoal
    'text_secondary': '#6B7280',   # Gray
    'text_light': '#FFFFFF',       # White text
    'border': '#D1D5DB',           # Light gray border
    'border_light': '#E5E7EB',     # Lighter border
    'accent_blue': '#3B82F6',      # Blue accent
    'accent_orange': '#F59E0B',    # Orange accent
    'accent_red': '#EF4444',       # Red accent
    'accent_purple': '#8B5CF6',    # Purple accent
    'hover_bg': '#F3F4F6',         # Hover background
    'table_header': '#2F5C46',     # Table header (same as primary)
    'table_alt_row': '#F9FAFB',    # Alternating row color
}

# Dark Theme Color Palette
DARK_COLORS = {
    'background': '#1F2937',       # Dark Blue-Grey
    'surface': '#111827',          # Darker Slate
    'primary': '#064E3B',          # Dark Emerald Green
    'primary_hover': '#065F46',    # Lighter Dark Green
    'primary_pressed': '#064E3B',  # Darker Emerald
    'text': '#F3F4F6',             # Off-White
    'text_secondary': '#9CA3AF',   # Light Gray
    'text_light': '#FFFFFF',       # White text
    'border': '#374151',           # Dark border
    'border_light': '#4B5563',     # Lighter dark border
    'accent_blue': '#60A5FA',      # Lighter Blue accent
    'accent_orange': '#FBBF24',    # Lighter Orange accent
    'accent_red': '#F87171',       # Lighter Red accent
    'accent_purple': '#A78BFA',    # Lighter Purple accent
    'hover_bg': '#374151',         # Dark Hover background
    'table_header': '#064E3B',     # Table header (dark green)
    'table_alt_row': '#1F2937',    # Alternating row color
}

# Default to light theme
COLORS = LIGHT_COLORS

def get_stylesheet(theme='light'):
    """
    Generate stylesheet for the given theme.
    
    Args:
        theme: 'light' or 'dark'
    
    Returns:
        Complete QSS stylesheet string
    """
    colors = DARK_COLORS if theme == 'dark' else LIGHT_COLORS
    
    return f"""
/* ============================================
   GLOBAL STYLES
   ============================================ */
QWidget {{
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
    font-size: 13px;
    color: {colors['text']};
}}

QMainWindow, #MainWindow {{
    background-color: {colors['background']};
}}

/* ============================================
   CUSTOM TITLE BAR
   ============================================ */
#TitleBar {{
    background-color: {colors['primary']};
    border: none;
    min-height: 40px;
    max-height: 40px;
}}

#TitleLabel {{
    color: {colors['text_light']};
    font-size: 15px;
    font-weight: bold;
    padding-left: 15px;
}}

#TitleBarButton {{
    background-color: transparent;
    border: none;
    color: {colors['text_light']};
    font-size: 16px;
    font-weight: bold;
    padding: 8px 15px;
    min-width: 45px;
}}

#TitleBarButton:hover {{
    background-color: rgba(255, 255, 255, 0.1);
}}

#CloseButton:hover {{
    background-color: {colors['accent_red']};
}}

/* ============================================
   SIDEBAR NAVIGATION
   ============================================ */
#Sidebar {{
    background-color: {colors['surface']};
    border-right: 1px solid {colors['border_light']};
    min-width: 200px;
    max-width: 200px;
}}

#SidebarTitle {{
    color: {colors['text_secondary']};
    font-size: 11px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 20px 15px 10px 15px;
}}

#NavButton {{
    background-color: transparent;
    border: none;
    border-radius: 8px;
    color: {colors['text']};
    font-size: 14px;
    font-weight: 500;
    padding: 12px 15px;
    text-align: left;
    margin: 2px 8px;
}}

#NavButton:hover {{
    background-color: {colors['hover_bg']};
}}

#NavButton:checked, #NavButton[active="true"] {{
    background-color: {colors['primary']};
    color: {colors['text_light']};
}}

/* ============================================
   CARDS (QFrame)
   ============================================ */
#Card {{
    background-color: {colors['surface']};
    border: 1px solid {colors['border_light']};
    border-radius: 12px;
    padding: 20px;
}}

#CardTitle {{
    color: {colors['text']};
    font-size: 16px;
    font-weight: bold;
    padding-bottom: 15px;
}}

#CardSubtitle {{
    color: {colors['text_secondary']};
    font-size: 12px;
    padding-bottom: 10px;
}}

/* ============================================
   SUMMARY CARDS
   ============================================ */
#SummaryCard {{
    background-color: {colors['surface']};
    border: 1px solid {colors['border_light']};
    border-radius: 12px;
    padding: 20px;
    min-height: 100px;
}}

#SummaryCard[accent="blue"] {{
    border-left: 4px solid {colors['accent_blue']};
}}

#SummaryCard[accent="green"] {{
    border-left: 4px solid {colors['primary']};
}}

#SummaryCard[accent="orange"] {{
    border-left: 4px solid {colors['accent_orange']};
}}

#SummaryCard[accent="red"] {{
    border-left: 4px solid {colors['accent_red']};
}}

#SummaryIcon {{
    font-size: 24px;
    padding: 5px;
}}

#SummaryTitle {{
    color: {colors['text_secondary']};
    font-size: 12px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

#SummaryValue {{
    font-size: 28px;
    font-weight: bold;
    padding: 5px 0;
}}

#SummaryValue[accent="blue"] {{
    color: {colors['accent_blue']};
}}

#SummaryValue[accent="green"] {{
    color: {colors['primary']};
}}

#SummaryValue[accent="orange"] {{
    color: {colors['accent_orange']};
}}

#SummaryValue[accent="red"] {{
    color: {colors['accent_red']};
}}

#SummaryUnit {{
    color: {colors['text_secondary']};
    font-size: 12px;
}}

/* ============================================
   BUTTONS
   ============================================ */
QPushButton {{
    background-color: {colors['primary']};
    border: none;
    border-radius: 8px;
    color: {colors['text_light']};
    font-size: 13px;
    font-weight: 600;
    padding: 10px 20px;
    min-height: 20px;
}}

QPushButton:hover {{
    background-color: {colors['primary_hover']};
}}

QPushButton:pressed {{
    background-color: {colors['primary_pressed']};
}}

QPushButton:disabled {{
    background-color: {colors['border']};
    color: {colors['text_secondary']};
}}

#SecondaryButton {{
    background-color: transparent;
    border: 2px solid {colors['primary']};
    color: {colors['primary']};
}}

#SecondaryButton:hover {{
    background-color: {colors['primary']};
    color: {colors['text_light']};
}}

#DangerButton {{
    background-color: {colors['accent_red']};
}}

#DangerButton:hover {{
    background-color: #DC2626;
}}

/* ============================================
   TABLES
   ============================================ */
QTableWidget {{
    background-color: {colors['surface']};
    border: none;
    border-radius: 8px;
    gridline-color: {colors['border_light']};
    selection-background-color: {colors['primary']};
    selection-color: {colors['text_light']};
}}

QTableWidget::item {{
    padding: 10px;
    border-bottom: 1px solid {colors['border_light']};
}}

QTableWidget::item:alternate {{
    background-color: {colors['table_alt_row']};
}}

QHeaderView::section {{
    background-color: {colors['table_header']};
    color: {colors['text_light']};
    font-weight: bold;
    font-size: 12px;
    padding: 12px 10px;
    border: none;
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}}

QHeaderView::section:first {{
    border-top-left-radius: 8px;
}}

QHeaderView::section:last {{
    border-top-right-radius: 8px;
    border-right: none;
}}

/* ============================================
   INPUTS & CONTROLS
   ============================================ */
QLineEdit {{
    background-color: {colors['surface']};
    border: 2px solid {colors['border']};
    border-radius: 8px;
    padding: 10px 15px;
    font-size: 13px;
}}

QLineEdit:focus {{
    border-color: {colors['primary']};
}}

QComboBox {{
    background-color: {colors['surface']};
    border: 2px solid {colors['border']};
    border-radius: 8px;
    padding: 8px 15px;
    font-size: 13px;
    min-width: 150px;
}}

QComboBox:focus {{
    border-color: {colors['primary']};
}}

QComboBox::drop-down {{
    border: none;
    padding-right: 10px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid {colors['text']};
    margin-right: 10px;
}}

QComboBox QAbstractItemView {{
    background-color: {colors['surface']};
    border: 1px solid {colors['border']};
    border-radius: 8px;
    selection-background-color: {colors['primary']};
    selection-color: {colors['text_light']};
}}

/* ============================================
   SCROLLBARS
   ============================================ */
QScrollBar:vertical {{
    background-color: transparent;
    width: 10px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background-color: {colors['border']};
    border-radius: 5px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {colors['text_secondary']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
    background: none;
}}

QScrollBar:horizontal {{
    background-color: transparent;
    height: 10px;
    margin: 0;
}}

QScrollBar::handle:horizontal {{
    background-color: {colors['border']};
    border-radius: 5px;
    min-width: 30px;
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
    background: none;
}}

/* ============================================
   TAB WIDGET (for content areas)
   ============================================ */
QTabWidget::pane {{
    background-color: transparent;
    border: none;
}}

QTabBar::tab {{
    background-color: transparent;
    color: {colors['text_secondary']};
    font-weight: 500;
    padding: 10px 20px;
    margin-right: 5px;
    border: none;
    border-bottom: 3px solid transparent;
}}

QTabBar::tab:selected {{
    color: {colors['primary']};
    border-bottom: 3px solid {colors['primary']};
}}

QTabBar::tab:hover:!selected {{
    color: {colors['text']};
}}

/* ============================================
   LABELS & TEXT
   ============================================ */
QLabel {{
    color: {colors['text']};
}}

#SectionTitle {{
    font-size: 18px;
    font-weight: bold;
    color: {colors['text']};
    padding-bottom: 15px;
}}

#SubText {{
    color: {colors['text_secondary']};
    font-size: 12px;
}}

/* ============================================
   LIST WIDGETS
   ============================================ */
QListWidget {{
    background-color: transparent;
    border: none;
    outline: none;
}}

QListWidget::item {{
    background-color: {colors['surface']};
    border: 1px solid {colors['border_light']};
    border-radius: 8px;
    margin: 5px 0;
    padding: 15px;
}}

QListWidget::item:hover {{
    border-color: {colors['primary']};
}}

QListWidget::item:selected {{
    background-color: {colors['primary']};
    color: {colors['text_light']};
}}

/* ============================================
   MESSAGE BOX
   ============================================ */
QMessageBox {{
    background-color: {colors['surface']};
}}

QMessageBox QLabel {{
    color: {colors['text']};
    font-size: 13px;
}}

/* ============================================
   PROGRESS BAR
   ============================================ */
QProgressBar {{
    background-color: {colors['border_light']};
    border: none;
    border-radius: 8px;
    height: 8px;
    text-align: center;
}}

QProgressBar::chunk {{
    background-color: {colors['primary']};
    border-radius: 8px;
}}

/* ============================================
   GROUP BOX
   ============================================ */
QGroupBox {{
    background-color: {colors['surface']};
    border: 1px solid {colors['border_light']};
    border-radius: 12px;
    margin-top: 20px;
    padding-top: 15px;
    font-weight: bold;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 15px;
    padding: 0 10px;
    color: {colors['text']};
    background-color: {colors['surface']};
}}

/* ============================================
   SPLITTER
   ============================================ */
QSplitter::handle {{
    background-color: transparent;
}}

QSplitter::handle:horizontal {{
    width: 8px;
}}

QSplitter::handle:vertical {{
    height: 8px;
}}
"""

# Keep backward compatibility
MAIN_STYLESHEET = get_stylesheet('light')

def get_matplotlib_style(theme='light'):
    """
    Get matplotlib styling based on theme.
    
    Args:
        theme: 'light' or 'dark'
    
    Returns:
        Dictionary with matplotlib style parameters
    """
    if theme == 'dark':
        return {
            'figure.facecolor': DARK_COLORS['surface'],
            'axes.facecolor': DARK_COLORS['surface'],
            'axes.edgecolor': DARK_COLORS['border'],
            'axes.labelcolor': DARK_COLORS['text'],
            'text.color': DARK_COLORS['text'],
            'xtick.color': DARK_COLORS['text_secondary'],
            'ytick.color': DARK_COLORS['text_secondary'],
            'grid.color': DARK_COLORS['border'],
        }
    else:
        return {
            'figure.facecolor': LIGHT_COLORS['surface'],
            'axes.facecolor': LIGHT_COLORS['surface'],
            'axes.edgecolor': LIGHT_COLORS['border'],
            'axes.labelcolor': LIGHT_COLORS['text'],
            'text.color': LIGHT_COLORS['text'],
            'xtick.color': LIGHT_COLORS['text_secondary'],
            'ytick.color': LIGHT_COLORS['text_secondary'],
            'grid.color': LIGHT_COLORS['border'],
        }


# Chart color palette
CHART_COLORS = [
    '#3B82F6',  # Blue
    '#10B981',  # Green
    '#F59E0B',  # Orange
    '#8B5CF6',  # Purple
    '#EF4444',  # Red
    '#06B6D4',  # Cyan
    '#EC4899',  # Pink
    '#6366F1',  # Indigo
]
