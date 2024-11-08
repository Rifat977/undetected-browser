from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os, zipfile, string, random, time
from fake_useragent import UserAgent

chrome_driver_path = "/home/rifat/.wdm/drivers/chromedriver/linux64/129.0.6668.70/chromedriver-linux64/chromedriver"

def create_proxy_auth_extension(proxy_host, proxy_port, proxy_user, proxy_pass, scheme='http', plugin_path='proxy_auth_plugin.zip'):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = string.Template(
        """
        var config = {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                    scheme: "${scheme}",
                    host: "${proxy_host}",
                    port: parseInt(${proxy_port})
                },
                bypassList: ["localhost", "127.0.0.1"]
            }
        };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${proxy_user}",
                    password: "${proxy_pass}"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ["blocking"]
        );
        """
    ).substitute(
        proxy_host=proxy_host,
        proxy_port=proxy_port,
        proxy_user=proxy_user,
        proxy_pass=proxy_pass,
        scheme=scheme,
    )

    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path

def get_webdriver_with_proxy(proxy_host, proxy_port, proxy_user, proxy_pass):
    ua = UserAgent()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--proxy-server=http://{proxy_host}:{proxy_port}')
    
    # Create proxy extension for authentication
    plugin_path = create_proxy_auth_extension(proxy_host, proxy_port, proxy_user, proxy_pass)
    chrome_options.add_extension(plugin_path)

    # Randomize user agent and set other options
    user_agent = ua.random
    chrome_options.add_argument("--head")  # Run Chrome in headless mode
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=1920,1080")

    
    service = Service(chrome_driver_path)

    try:
        browser = webdriver.Chrome(service=service, options=chrome_options)
        return browser
    except Exception as e:
        print(f"Failed to start Chrome with error: {e}")
        return None

def get_webdriver_without_proxy():
    ua = UserAgent()
    chrome_options = webdriver.ChromeOptions()

    # Randomize user agent and set other options
    user_agent = ua.random
    chrome_options.add_argument("--head")  # Run Chrome in headless mode
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=1920,1080")

    service = Service(chrome_driver_path)

    try:
        browser = webdriver.Chrome(service=service, options=chrome_options)
        return browser
    except Exception as e:
        print(f"Failed to start Chrome with error: {e}")
        return None


def parse_proxy_string(proxy_string):
    parts = proxy_string.split(':')
    if len(parts) != 4:
        raise ValueError("Invalid proxy format. Expecting 'host:port:user:pass'.")
    
    return parts[0], parts[1], parts[2], parts[3]

def fetch_ip_using_proxy(proxy_string=None, browser_name=None):
    try:
        if proxy_string:
            proxy_host, proxy_port, proxy_user, proxy_pass = parse_proxy_string(proxy_string)
            browser = get_webdriver_with_proxy(proxy_host, proxy_port, proxy_user, proxy_pass)
        else:
            browser = get_webdriver_without_proxy()

        if browser:
            first_url = "https://whoer.net/"
            browser.get(first_url)
            time.sleep(2)
            
            if browser_name:
                browsers[browser_name] = browser  # Store the browser instance with a name
            return "Browser Created"
        else:
            return "Failed to start browser."
    except Exception as e:
        return f"Error: {e}"
