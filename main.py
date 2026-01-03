import time
from datetime import datetime, timezone
from selenium.common.exceptions import InvalidSessionIdException, WebDriverException

from config import DHMZ_URL, REFRESH_SECONDS, HEADLESS, PAGE_LOAD_TIMEOUT, WAIT_AFTER_LOAD
from scraper import create_driver, fetch_html
from parser import parse_measurements
from storage import save_record

def now_utc_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def run():
    print("START: otvaram Chrome...")
    driver = create_driver(headless=HEADLESS, page_load_timeout=PAGE_LOAD_TIMEOUT)
    print("Chrome otvoren. Otvaram DHMZ stranicu...")
    print("URL:", DHMZ_URL)

    while True:
        try:
            html = fetch_html(driver, DHMZ_URL, WAIT_AFTER_LOAD)
            measurements = parse_measurements(html)

            record = {
                "timestamp_utc": now_utc_iso(),
                "source_url": DHMZ_URL,
                "count": len(measurements),
                "measurements": measurements
            }

            total_24h = save_record(record)
            print(f"OK: {len(measurements)} mjerenja | spremljeno u data/measurements.json | ukupno zapisa(24h): {total_24h}")

            time.sleep(REFRESH_SECONDS)

        except KeyboardInterrupt:
            print("STOP: prekinuto (Ctrl+C). KRAJ.")
            try:
                driver.quit()
            except Exception:
                pass
            break

        except InvalidSessionIdException:
            try:
                driver.quit()
            except Exception:
                pass
            driver = create_driver(headless=HEADLESS, page_load_timeout=PAGE_LOAD_TIMEOUT)

        except WebDriverException as e:
            print("ERROR (WebDriver):", e)
            time.sleep(3)

        except Exception as e:
            print("ERROR:", e)
            time.sleep(3)

if __name__ == "__main__":
    run()
