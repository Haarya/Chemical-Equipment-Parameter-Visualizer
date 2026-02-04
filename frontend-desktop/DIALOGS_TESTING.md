# Login and Register Dialog Testing Guide

## Testing the Dialogs

The PyQt5 desktop application now includes fully functional login and register dialogs.

### What Was Created:

1. **login_dialog.py** - Login Dialog
   - Username and password fields
   - Login button with API authentication
   - Register button to switch to registration
   - Error messages for invalid credentials
   - Connection error handling
   - Auto-focus on username field
   - Enter key support for quick login

2. **register_dialog.py** - Registration Dialog
   - Username, email, password fields
   - Password confirmation field
   - Input validation (email format, password match, etc.)
   - Error messages with detailed feedback
   - Success message with auto-login
   - Cancel button to return to login

3. **Updated main_window.py**
   - Integrated API service
   - Login dialog shown on startup
   - Login menu action with conflict handling
   - Logout with confirmation
   - Status bar updates

### Features Implemented:

✅ **Login Dialog:**
- Clean, professional UI with Reactometrix branding
- Username and password input fields
- "Login" button calls backend API
- "Register" button opens registration dialog
- Error handling for:
  - Invalid credentials (400/401 errors)
  - Connection errors (backend not running)
  - Server errors
- Loading state during authentication
- Signal emitted on successful login
- Enter key support

✅ **Register Dialog:**
- Username, email, password, confirm password fields
- Comprehensive validation:
  - Username: min 3 chars, alphanumeric + underscore
  - Email: valid format check
  - Password: min 3 chars, must match confirmation
- Error messages for each validation rule
- Success message with auto-login after registration
- API error handling (duplicate username/email)
- Loading state during registration
- Signal emitted on successful registration

✅ **Integration:**
- Login dialog auto-shows on startup
- Successful login stores token in APIService
- Status bar shows current user
- Menu actions updated based on login state
- Logout clears token and resets UI

### Testing Steps:

1. **Start Backend Server:**
   ```bash
   cd backend
   venv\Scripts\activate
   python manage.py runserver
   ```

2. **Run Desktop App:**
   ```bash
   cd frontend-desktop
   venv\Scripts\python.exe main.py
   ```

3. **Test Registration:**
   - Click "Register" button
   - Fill in: username (e.g., "testuser"), email, password
   - Click "Register"
   - Should auto-login and show success message

4. **Test Login:**
   - Use existing credentials (e.g., "Haarya" / "123")
   - Click "Login"
   - Should show welcome message and update status bar

5. **Test Error Cases:**
   - Try invalid credentials → Should show error
   - Try registering duplicate username → Should show error
   - Stop backend and try login → Should show connection error

### Visual Design:

- Modern, clean interface with grouped form fields
- Color-coded buttons (green for primary, gray for secondary)
- Error messages in red with light red background
- Success messages in green with light green background
- Proper spacing and alignment
- Responsive button states (hover, pressed, disabled)
- 400x300 login dialog, 450x400 register dialog

### Next Steps:

The dialogs are complete and functional. You can now:
1. Test the authentication flow with your Django backend
2. Implement the upload widget (Step 4.4)
3. Create data table widget (Step 4.5)
4. Build chart components (Step 4.6)

### Notes:

- Both dialogs use PyQt5 signals to communicate with main window
- API service handles token storage automatically
- Error messages are user-friendly and specific
- All inputs are validated before API calls
- Loading states prevent double-submission
