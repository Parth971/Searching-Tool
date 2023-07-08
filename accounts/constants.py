# Error
PASSWORD_MISMATCH = "Password fields didn't match"
INVALID_EMAIL = "Email not valid"
INCORRECT_OLD_PASSWORD = "Old password is not correct"
PASSWORD_SPECIAL_SYMBOL_ERROR = 'Password must contain at-least one special symbol'
PASSWORD_DIGIT_ERROR = 'Password must contain at-least one digit'
PASSWORD_UPPERCASE_LETTER_ERROR = 'Password must contain at-least one uppercase letter'
PASSWORD_LOWERCASE_LETTER_ERROR = 'Password must contain at-least one lowercase letter'
FIRST_NAME_ERROR = 'First name must contain alphabets and space only'
LAST_NAME_ERROR = 'Last name must contain alphabets and space only'
FIRST_NAME_LENGTH_ERROR = 'First name should have length between 3 to 20'
LAST_NAME_LENGTH_ERROR = 'Last name should have length between 3 to 20'
INVALID_PHONE_NUMBER = 'Mobile number is not valid'
EMAIL_NOT_ACTIVATED = "Email is not active"
EMAIL_ALREADY_ACTIVATED = "Email is already active"
EMAIL_NOT_UNIQUE = "Email is already used"
EMAIL_REQUIRED_ERROR = 'Email is required'
PASSWORD_REQUIRED_ERROR = 'Password is required'
FIRST_NAME_REQUIRED_ERROR = 'First name is required'
LAST_NAME_REQUIRED_ERROR = 'Last name is required'
MOBILE_NUMBER_REQUIRED_ERROR = 'Mobile number is required'
JOB_TITLE_REQUIRED_ERROR = 'Job title is required'
COMPANY_NAME_REQUIRED_ERROR = 'Company name is required'
PROFILE_PIC_REQUIRED_ERROR = 'Profile picture is required'
INVALID_UID = 'UID Invalid'
INVALID_TOKEN = 'Token Invalid'
LOGIN_FAILED = "No active account found with the given credentials"

# Help text
PASSWORD_HELP_TEXT = 'Password must contain 1 special char, 1 digit, 1 small alphabet, and 1 capital alphabet'

# Validation Regex
SPECIAL_SYMBOL_REGEX = "(?=.*?[#?!@$%^&*-])"
DIGIT_REGEX = "(?=.*?[0-9])"
UPPERCASE_LETTER_REGEX = "(?=.*?[A-Z])"
LOWERCASE_LETTER_REGEX = "(?=.*?[a-z])"
USER_NAME_REGEX = "^[a-zA-Z ]+$"  # Used for both first_name and last_name field in User model
PHONE_NUMBER_REGEX = "^\\+?[1-9][0-9]{7,14}$"

# Message
RESTORE_PASSWORD_LINK_SENT = "Restore password link has been sent to email"
EMAIL_VERIFICATION_LINK_SENT = "Email verification link has been sent to email"
EMAIL_VERIFIED_SUCCESS = "Email verification successful"
REGISTER_SUCCESS = "Registered successfully, now you can verify from link sent"
PASSWORD_CHANGED_SUCCESS = "Password changed successfully"
LOGIN_SUCCESS = "Successfully logged in"
LOGOUT_SUCCESS = "Successfully logged out"
REFRESH_TOKEN_SUCCESS = "Access token refreshed successfully"
PROFILE_UPDATE_SUCCESS = 'Profile updated successfully'
PROFILE_PIC_UPDATE_SUCCESS = 'Profile picture updated successfully'
PROFILE_PIC_DELETE_SUCCESS = 'Profile picture deleted successfully'

# Variables
FIRST_NAME_MINIMUM_LENGTH = LAST_NAME_MINIMUM_LENGTH = 3
FIRST_NAME_MAXIMUM_LENGTH = LAST_NAME_MAXIMUM_LENGTH = 20

# Path
DEFAULT_PROFILE_PIC_PATH = '/static/accounts/images/default_profile_pic.jpg'
