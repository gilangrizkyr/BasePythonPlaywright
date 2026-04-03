"""Locators untuk berbagai page objects"""

class CommonLocators:
    """Common locators yang dapat digunakan di semua page"""
    BODY = "body"
    LOADER = '[role="progressbar"]'
    ERROR_MESSAGE = '[role="alert"]'


class LoginPageLocators:
    """Locators untuk Login Page"""
    USERNAME_INPUT = 'input[name="username"]'
    PASSWORD_INPUT = 'input[name="password"]'
    LOGIN_BUTTON = 'button:has-text("Login")'
    ERROR_MESSAGE = '.error-message'
    FORGOT_PASSWORD_LINK = 'a:has-text("Forgot Password")'


class HomePageLocators:
    """Locators untuk Home Page"""
    WELCOME_MESSAGE = '.welcome-title'
    USER_PROFILE_ICON = '[aria-label="User Profile"]'
    LOGOUT_BUTTON = 'button:has-text("Logout")'
    NAVIGATION_MENU = 'nav[role="navigation"]'


class DashboardLocators:
    """Locators untuk Dashboard"""
    DASHBOARD_TITLE = 'h1:has-text("Dashboard")'
    STAT_CARDS = '[class*="stat-card"]'
    CHART_CONTAINER = '[class*="chart"]'
    TABLE_ROWS = 'table tbody tr'
    EXPORT_BUTTON = 'button:has-text("Export")'
