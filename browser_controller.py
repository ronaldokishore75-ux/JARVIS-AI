# =========================================================
# JARVIS BROWSER CONTROLLER
# Dedicated Playwright thread
# =========================================================

from playwright.sync_api import sync_playwright

import os
import queue
import threading
import traceback


class BrowserController:

    def __init__(self):

        self._jobs = queue.Queue()

        self._thread = None
        self._ready = threading.Event()

        self._playwright = None
        self._browser = None
        self._page = None

        self._startup_error = None

    # =====================================================
    # CREATE / RECREATE BROWSER
    # =====================================================

    def _create_browser(self):

        profile_path = os.path.join(
            os.path.dirname(__file__),
            "jarvis_browser_profile"
        )

        self._browser = (
            self._playwright
            .chromium
            .launch_persistent_context(
                user_data_dir=profile_path,
                headless=False
            )
        )

        if self._browser.pages:

            self._page = self._browser.pages[0]

        else:

            self._page = self._browser.new_page()

        print(
            "Persistent JARVIS browser session ready."
        )

    # =====================================================
    # START BROWSER WORKER
    # =====================================================

    def start(self):

        if (
            self._thread is None
            or not self._thread.is_alive()
        ):

            self._ready.clear()
            self._startup_error = None

            self._thread = threading.Thread(
                target=self._browser_worker,
                name="JarvisPlaywrightThread",
                daemon=True
            )

            self._thread.start()

        self._ready.wait()

        if self._startup_error:

            raise RuntimeError(
                self._startup_error
            )

        return True

    # =====================================================
    # PLAYWRIGHT WORKER THREAD
    # =====================================================

    def _browser_worker(self):

        try:

            # IMPORTANT:
            # Playwright must be created inside this thread.
            self._playwright = sync_playwright().start()

            self._create_browser()

            self._ready.set()

            print(
                "Persistent JARVIS browser session started."
            )

            # -------------------------------------------------
            # Process browser jobs forever
            # -------------------------------------------------

            while True:

                job = self._jobs.get()

                if job is None:
                    break

                (
                    function,
                    args,
                    kwargs,
                    result_event,
                    result_box
                ) = job

                try:

                    # -----------------------------------------
                    # Recover closed browser/page
                    # -----------------------------------------

                    if (
                        self._browser is None
                        or self._browser.is_closed()
                        or self._page is None
                        or self._page.is_closed()
                    ):

                        print(
                            "Browser was closed. "
                            "Restarting JARVIS browser..."
                        )

                        self._create_browser()

                    result = function(
                        *args,
                        **kwargs
                    )

                    result_box["result"] = result

                except Exception as error:

                    result_box["error"] = error

                    print(
                        "BROWSER THREAD ERROR:"
                    )

                    traceback.print_exc()

                finally:

                    result_event.set()

        except Exception as error:

            self._startup_error = (
                f"Could not start browser: {error}"
            )

            self._ready.set()

            print(
                self._startup_error
            )

            traceback.print_exc()

    # =====================================================
    # RUN FUNCTION ON PLAYWRIGHT THREAD
    # =====================================================

    def _call(
        self,
        function,
        *args,
        **kwargs
    ):

        self.start()

        result_event = threading.Event()

        result_box = {}

        self._jobs.put(
            (
                function,
                args,
                kwargs,
                result_event,
                result_box
            )
        )

        result_event.wait()

        if "error" in result_box:

            raise result_box["error"]

        return result_box.get("result")

    # =====================================================
    # OPEN URL
    # =====================================================

    def open_url(self, url):

        def job():

            self._page.goto(
                url,
                wait_until="domcontentloaded"
            )

            return True

        return self._call(job)

    # =====================================================
    # GOOGLE SEARCH
    # =====================================================

    def search_google(self, query):

        def job():

            self._page.goto(
                "https://www.google.com",
                wait_until="domcontentloaded"
            )

            self._page.wait_for_timeout(1500)

            search_box = self._page.locator(
                "textarea[name='q']"
            )

            search_box.fill(query)

            search_box.press("Enter")

            return True

        return self._call(job)

    # =====================================================
    # OPEN YOUTUBE
    # =====================================================

    def open_youtube(self):

        def job():

            self._page.goto(
                "https://www.youtube.com",
                wait_until="domcontentloaded"
            )

            print(
                "YouTube opened in persistent JARVIS browser."
            )

            return True

        return self._call(job)

    # =====================================================
    # SEARCH YOUTUBE
    # =====================================================

    def search_youtube(self, query):

        def job():

            self._page.goto(
                "https://www.youtube.com",
                wait_until="domcontentloaded"
            )

            self._page.wait_for_timeout(2000)

            search_box = self._page.locator(
                'input[name="search_query"]'
            )

            search_box.fill(query)

            search_box.press("Enter")

            return True

        return self._call(job)

    # =====================================================
    # SCROLL DOWN
    # =====================================================

    def scroll_down(self):

        def job():

            self._page.mouse.wheel(
                0,
                1000
            )

            return True

        return self._call(job)

    # =====================================================
    # SCROLL UP
    # =====================================================

    def scroll_up(self):

        def job():

            self._page.mouse.wheel(
                0,
                -1000
            )

            return True

        return self._call(job)

    # =====================================================
    # SMALL SCROLL DOWN
    # =====================================================

    def scroll_down_little(self):

        def job():

            self._page.mouse.wheel(
                0,
                300
            )

            return True

        return self._call(job)

    # =====================================================
    # SMALL SCROLL UP
    # =====================================================

    def scroll_up_little(self):

        def job():

            self._page.mouse.wheel(
                0,
                -300
            )

            return True

        return self._call(job)

    # =====================================================
    # CLICK LINK
    # =====================================================

    def click_link(self, name):

        def job():

            print(
                f"Looking for: {name}"
            )

            link = self._page.locator(
                f'a:has-text("{name}")'
            ).first

            link.wait_for(
                state="visible",
                timeout=10000
            )

            href = link.get_attribute(
                "href"
            )

            print(
                f"Found href: {href}"
            )

            if not href:

                print(
                    "No valid href found."
                )

                return False

            if href.startswith("/"):

                href = (
                    "https://www.youtube.com"
                    + href
                )

            print(
                f"Opening: {href}"
            )

            self._page.goto(
                href,
                wait_until="domcontentloaded"
            )

            return True

        return self._call(job)


# =========================================================
# ONE SHARED BROWSER CONTROLLER
# =========================================================

browser_controller = BrowserController()