"""
Example Test Pages
==================

Example page classes demonstrating the professional framework usage.
"""

from core.base import BasePage, BaseElement
from core.config import config


class LoginPage(BasePage):
    """Example login page"""

    def _init_elements(self) -> None:
        """Initialize page elements"""
        self.add_element("username_input", "#username", "Username input field")
        self.add_element("password_input", "#password", "Password input field")
        self.add_element("login_button", "#login-btn", "Login button")
        self.add_element("error_message", ".error-message", "Error message")
        self.add_element("forgot_password_link", "a[href='/forgot-password']", "Forgot password link")

    def get_page_elements(self) -> dict:
        """Get page elements mapping"""
        return {
            "username_input": "#username",
            "password_input": "#password",
            "login_button": "#login-btn",
            "error_message": ".error-message",
            "forgot_password_link": "a[href='/forgot-password']",
        }

    async def is_loaded(self) -> bool:
        """Check if login page is loaded"""
        return await self.get_element("username_input").is_visible()

    async def login(self, username: str, password: str) -> None:
        """Perform login action"""
        await self.get_element("username_input").fill(username)
        await self.get_element("password_input").fill(password)
        await self.get_element("login_button").click()

    async def get_error_message(self) -> str:
        """Get error message text"""
        return await self.get_element("error_message").get_text()

    async def click_forgot_password(self) -> None:
        """Click forgot password link"""
        await self.get_element("forgot_password_link").click()


class DashboardPage(BasePage):
    """Example dashboard page"""

    def _init_elements(self) -> None:
        """Initialize page elements"""
        self.add_element("welcome_message", ".welcome-message", "Welcome message")
        self.add_element("user_menu", ".user-menu", "User menu")
        self.add_element("logout_button", "#logout-btn", "Logout button")
        self.add_element("dashboard_cards", ".dashboard-card", "Dashboard cards")
        self.add_element("notifications_badge", ".notifications-badge", "Notifications badge")

    def get_page_elements(self) -> dict:
        """Get page elements mapping"""
        return {
            "welcome_message": ".welcome-message",
            "user_menu": ".user-menu",
            "logout_button": "#logout-btn",
            "dashboard_cards": ".dashboard-card",
            "notifications_badge": ".notifications-badge",
        }

    async def is_loaded(self) -> bool:
        """Check if dashboard page is loaded"""
        return await self.get_element("welcome_message").is_visible()

    async def get_welcome_message(self) -> str:
        """Get welcome message"""
        return await self.get_element("welcome_message").get_text()

    async def logout(self) -> None:
        """Perform logout"""
        await self.get_element("user_menu").click()
        await self.get_element("logout_button").click()

    async def get_dashboard_cards_count(self) -> int:
        """Get number of dashboard cards"""
        cards = self.page.locator(".dashboard-card")
        return await cards.count()

    async def get_notifications_count(self) -> int:
        """Get notifications count"""
        badge_text = await self.get_element("notifications_badge").get_text()
        try:
            return int(badge_text)
        except ValueError:
            return 0


class ProductPage(BasePage):
    """Example product page"""

    def _init_elements(self) -> None:
        """Initialize page elements"""
        self.add_element("product_title", ".product-title", "Product title")
        self.add_element("product_price", ".product-price", "Product price")
        self.add_element("add_to_cart_button", "#add-to-cart-btn", "Add to cart button")
        self.add_element("product_image", ".product-image", "Product image")
        self.add_element("product_description", ".product-description", "Product description")
        self.add_element("quantity_input", "#quantity", "Quantity input")
        self.add_element("reviews_section", ".reviews-section", "Reviews section")

    def get_page_elements(self) -> dict:
        """Get page elements mapping"""
        return {
            "product_title": ".product-title",
            "product_price": ".product-price",
            "add_to_cart_button": "#add-to-cart-btn",
            "product_image": ".product-image",
            "product_description": ".product-description",
            "quantity_input": "#quantity",
            "reviews_section": ".reviews-section",
        }

    async def is_loaded(self) -> bool:
        """Check if product page is loaded"""
        return await self.get_element("product_title").is_visible()

    async def get_product_title(self) -> str:
        """Get product title"""
        return await self.get_element("product_title").get_text()

    async def get_product_price(self) -> str:
        """Get product price"""
        return await self.get_element("product_price").get_text()

    async def add_to_cart(self, quantity: int = 1) -> None:
        """Add product to cart"""
        if quantity > 1:
            await self.get_element("quantity_input").fill(str(quantity))
        await self.get_element("add_to_cart_button").click()

    async def get_product_description(self) -> str:
        """Get product description"""
        return await self.get_element("product_description").get_text()

    async def is_image_loaded(self) -> bool:
        """Check if product image is loaded"""
        img_element = await self.get_element("product_image").get_element_handle()
        return await self.page.evaluate("""
            (img) => {
                return img.complete && img.naturalHeight !== 0;
            }
        """, img_element)


class CheckoutPage(BasePage):
    """Example checkout page"""

    def _init_elements(self) -> None:
        """Initialize page elements"""
        self.add_element("checkout_form", ".checkout-form", "Checkout form")
        self.add_element("first_name_input", "#first-name", "First name input")
        self.add_element("last_name_input", "#last-name", "Last name input")
        self.add_element("email_input", "#email", "Email input")
        self.add_element("address_input", "#address", "Address input")
        self.add_element("city_input", "#city", "City input")
        self.add_element("zip_input", "#zip", "ZIP code input")
        self.add_element("card_number_input", "#card-number", "Card number input")
        self.add_element("expiry_input", "#expiry", "Expiry date input")
        self.add_element("cvv_input", "#cvv", "CVV input")
        self.add_element("place_order_button", "#place-order-btn", "Place order button")
        self.add_element("order_summary", ".order-summary", "Order summary")

    def get_page_elements(self) -> dict:
        """Get page elements mapping"""
        return {
            "checkout_form": ".checkout-form",
            "first_name_input": "#first-name",
            "last_name_input": "#last-name",
            "email_input": "#email",
            "address_input": "#address",
            "city_input": "#city",
            "zip_input": "#zip",
            "card_number_input": "#card-number",
            "expiry_input": "#expiry",
            "cvv_input": "#cvv",
            "place_order_button": "#place-order-btn",
            "order_summary": ".order-summary",
        }

    async def is_loaded(self) -> bool:
        """Check if checkout page is loaded"""
        return await self.get_element("checkout_form").is_visible()

    async def fill_billing_info(self, billing_info: dict) -> None:
        """Fill billing information"""
        await self.get_element("first_name_input").fill(billing_info.get("first_name", ""))
        await self.get_element("last_name_input").fill(billing_info.get("last_name", ""))
        await self.get_element("email_input").fill(billing_info.get("email", ""))
        await self.get_element("address_input").fill(billing_info.get("address", ""))
        await self.get_element("city_input").fill(billing_info.get("city", ""))
        await self.get_element("zip_input").fill(billing_info.get("zip", ""))

    async def fill_payment_info(self, payment_info: dict) -> None:
        """Fill payment information"""
        await self.get_element("card_number_input").fill(payment_info.get("card_number", ""))
        await self.get_element("expiry_input").fill(payment_info.get("expiry", ""))
        await self.get_element("cvv_input").fill(payment_info.get("cvv", ""))

    async def place_order(self) -> None:
        """Place the order"""
        await self.get_element("place_order_button").click()

    async def get_order_summary_text(self) -> str:
        """Get order summary text"""
        return await self.get_element("order_summary").get_text()


class SearchPage(BasePage):
    """Example search page"""

    def _init_elements(self) -> None:
        """Initialize page elements"""
        self.add_element("search_input", "#search-input", "Search input field")
        self.add_element("search_button", "#search-btn", "Search button")
        self.add_element("search_results", ".search-results", "Search results container")
        self.add_element("result_items", ".result-item", "Individual result items")
        self.add_element("no_results_message", ".no-results", "No results message")
        self.add_element("filter_dropdown", ".filter-dropdown", "Filter dropdown")
        self.add_element("sort_dropdown", ".sort-dropdown", "Sort dropdown")

    def get_page_elements(self) -> dict:
        """Get page elements mapping"""
        return {
            "search_input": "#search-input",
            "search_button": "#search-btn",
            "search_results": ".search-results",
            "result_items": ".result-item",
            "no_results_message": ".no-results",
            "filter_dropdown": ".filter-dropdown",
            "sort_dropdown": ".sort-dropdown",
        }

    async def is_loaded(self) -> bool:
        """Check if search page is loaded"""
        return await self.get_element("search_input").is_visible()

    async def perform_search(self, query: str) -> None:
        """Perform search"""
        await self.get_element("search_input").fill(query)
        await self.get_element("search_button").click()

    async def get_search_results_count(self) -> int:
        """Get number of search results"""
        results = self.page.locator(".result-item")
        return await results.count()

    async def get_result_titles(self) -> list:
        """Get list of result titles"""
        titles = []
        result_items = self.page.locator(".result-item .title")
        count = await result_items.count()

        for i in range(count):
            title = await result_items.nth(i).text_content()
            if title:
                titles.append(title.strip())

        return titles

    async def click_result_by_index(self, index: int) -> None:
        """Click on search result by index"""
        result_items = self.page.locator(".result-item")
        await result_items.nth(index).click()

    async def is_no_results_visible(self) -> bool:
        """Check if no results message is visible"""
        return await self.get_element("no_results_message").is_visible()

    async def apply_filter(self, filter_value: str) -> None:
        """Apply search filter"""
        await self.get_element("filter_dropdown").select_option(filter_value)

    async def apply_sort(self, sort_value: str) -> None:
        """Apply search sort"""
        await self.get_element("sort_dropdown").select_option(sort_value)