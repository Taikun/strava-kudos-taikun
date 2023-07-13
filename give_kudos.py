import os
import time
import send_telegram
from jproperties import Properties
import traceback
from dotenv import load_dotenv, find_dotenv


from playwright.sync_api import sync_playwright, TimeoutError
from playwright.async_api import async_playwright


BASE_URL = "https://www.strava.com/"


load_dotenv(find_dotenv())
STRAVA_EMAIL = os.getenv('STRAVA_EMAIL')
STRAVA_PASSWORD = os.getenv('STRAVA_PASSWORD')


class KudosGiver:
    """
    Logins into Strava and gives kudos to all activities under
    Following. Additionally, scrolls down to check for more activities
    until no more kudos can be given at this time.
    """

    def __init__(self, max_retry_scroll=3, max_run_duration=540) -> None:
        if STRAVA_EMAIL is None or STRAVA_PASSWORD is None:
            raise Exception(
                f"EMAIL AND PASSWORD configuration missing. \
                check configuration file in server"
            )
        self.max_retry_scroll = max_retry_scroll
        self.max_run_duration = max_run_duration
        self.kudos_button_pattern = '[data-testid="kudos_button"]'
        p = sync_playwright().start()
        self.browser = p.firefox.launch()  # does not work in chrome
        self.page = self.browser.new_page()

        self.start_time = time.time()

    def email_login(self):
        """
        Login using email and password
        """
        self.page.goto(os.path.join(BASE_URL, "login"))
        self.page.fill("#email", STRAVA_EMAIL)
        self.page.fill("#password", STRAVA_PASSWORD)
        self.page.click("button[type='submit']")
        print("---Logged in!!---")
        self.page.goto(
            os.path.join(BASE_URL, "dashboard"), wait_until="domcontentloaded"
        )

    def locate_kudos_buttons_and_maybe_give_kudos(self, button_locator) -> int:
        """
        input: playwright.locator class
        Returns count of kudos given.
        """
        b_count = button_locator.count()
        given_count = 0
        for i in range(b_count):
            button = button_locator.nth(i)
            if button.get_by_test_id("unfilled_kudos").count():
                try:
                    button.click(timeout=2000)
                    given_count += 1
                    time.sleep(1)
                except TimeoutError:
                    print("Click timed out.")
        print(f"Kudos given: {given_count}")
        return given_count

    def give_kudos(self):
        """
        Scroll through pages to give kudos that are giveable.
        """
        try:
            ## Give Kudos on loaded page ##
            button_locator = self.page.locator(self.kudos_button_pattern)
            kudos_given = self.locate_kudos_buttons_and_maybe_give_kudos(
                button_locator=button_locator
            )
            curr_retry = self.max_retry_scroll

            ## Scroll down and repeat ##
            while kudos_given or curr_retry > 0:
                curr_duration = time.time() - self.start_time
                if curr_duration > self.max_run_duration:
                    print("Max run duration reached.")
                    break
                self.page.mouse.wheel(0, 12000)
                time.sleep(5)
                kudos_given = self.locate_kudos_buttons_and_maybe_give_kudos(
                    button_locator=button_locator
                )
                if not kudos_given:
                    curr_retry -= 1
            self.browser.close()
            print("That's all, folks! Terminating... ")
        except Exception as e:
            print(traceback.format_exc())

    def __del__(self):
        print("I'm being automatically destroyed. Goodbye!")


def main():
    send_telegram.send_to_telegram("Trying to give kudos")
    kg = KudosGiver()
    kg.email_login()
    kg.give_kudos()


# to call from FAST API
async def fromAPI():
    send_telegram.send_to_telegram("Trying to give kudos")
    kg = KudosGiver()
    kg.email_login()
    kg.give_kudos()

    return "Request Finished"


if __name__ == "__main__":
    main()
