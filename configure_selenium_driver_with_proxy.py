# Function for configuring a working selenium driver with optimized options which I found to work best with mimicking real user behaviour
# Options, fingerprint and other parameters are up-to-date and still working as of 01/04/2025
# To be used with a proxy connection (passed as a hostname)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium_authenticated_proxy import SeleniumAuthenticatedProxy

def configure_webdriver(proxy_url:str):
    """
    Webdriver, user agent, fingerprint and Chrome browser configuration.
    Returns configured webdriver.
    """

    # Browser initiation options
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome"
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--start-fullscreen")
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")

    # WebDriver configuration and initiation
    if proxy_url:
        proxy_helper = SeleniumAuthenticatedProxy(proxy_url=proxy_url)
        proxy_helper.enrich_chrome_options(chrome_options)
    service = Service(executable_path=DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Partially disable webrtc
    preferences = {
        "webrtc.ip_handling_policy" : "disable_non_proxied_udp",
        "webrtc.multiple_routes_enabled": False,
        "webrtc.nonproxied_udp_enabled" : False
    }
    chrome_options.add_experimental_option("prefs", preferences)

    return driver

