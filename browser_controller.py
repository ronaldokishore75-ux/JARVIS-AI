from playwright.sync_api import sync_playwright
import os

class BrowserController:

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

    def start(self):

        if self.browser is None:

            self.playwright = sync_playwright().start()

        # Dedicated persistent profile for JARVIS
            profile_path = os.path.join(
                os.path.dirname(__file__),
                "jarvis_browser_profile"
            )

            self.browser = self.playwright.chromium.launch_persistent_context(
                user_data_dir=profile_path,
            headless=False
            )

            # Get the existing page or create one
            if self.browser.pages:
                self.page = self.browser.pages[0]
            else:
                self.page = self.browser.new_page()

            print("Persistent JARVIS browser session started.")

        return self.page


    def open_url(self, url):

        self.start()

        self.page.goto(url)

    def search_google(self, query):

        self.start()

        self.page.goto("https://www.google.com")

        self.page.fill(
            "textarea[name='q']",
            query
        )

        self.page.keyboard.press("Enter")


    def open_youtube(self):

        self.start()

        self.page.goto("https://www.youtube.com")

        print("YouTube opened in persistent JARVIS browser.")





    

    def search_youtube(self, query):

        self.start()

        self.page.goto("https://www.youtube.com")

        self.page.wait_for_timeout(2000)

        search_box = self.page.locator(
            'input[name="search_query"]'
        )

        search_box.fill(query)

        search_box.press("Enter")

    def scroll_down(self):

        self.start()

        self.page.mouse.wheel(0, 1000)

    def scroll_up(self):

        self.start()

        self.page.mouse.wheel(0, -1000)

    def scroll_down_little(self):

        self.start()

        self.page.mouse.wheel(0, 300)

    def scroll_up_little(self):

        self.start()

        self.page.mouse.wheel(0, -300)

    def click_link(self, name):

        self.start()

        print(f"Looking for: {name}")

    # Find a visible link containing the name

        link = self.page.locator(
            f'a:has-text("{name}")'
        ).first

    # Wait until the link exists

        link.wait_for(state="visible", timeout=10000)

    # Print the actual URL before clicking

        href = link.get_attribute("href")

        print(f"Found href: {href}")

        if href:


            # Convert relative YouTube links into full URLs

            if href.startswith("/"):
                href = "https://www.youtube.com" + href

            print(f"Opening: {href}")

            self.page.goto(href)

        else:
            print("No valid href found.")




# One shared browser session
browser_controller = BrowserController()