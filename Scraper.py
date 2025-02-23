import os
import time
import json
import random
import requests
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# List of URLs to scrape
URLS = [
    "https://www.renesas.com/en/applications/automotive/adas/adas-front-camera-solution#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/adas/intelligent-camera-solution#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/adas/automotive-camera-solution-ahl-control-channel#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/adas/comprehensive-adas-autonomous-driving-hardware-software-system#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/adas/parking-assistance-system-ahl-camera#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/adas/video-output-expansion-surround-vie-ar-hud#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/ev-hev-vehicles/bi-directional-dcdc-converter-12v-48v-ev-hev-systems#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/ev-hev-vehicles/bi-directional-gan-dcdc-converter-12v48v-evhev-systems#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/ev-hev-vehicles/3-1-electric-vehicle-unit-48v-inverter-onboard-charger-dcdc-converter#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/ev-hev-vehicles/standard-ev-battery-management-system#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/ev-hev-vehicles/wireless-ev-battery-management-system#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/ev-hev-vehicles/level-2-ev-charger#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/ev-hev-vehicles/48v-3kw-motor-control-2-3-wheelers#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/ev-hev-vehicles/xev-inverter#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/ev-hev-vehicles/low-voltage-inverter-2-3-wheeler-traction-motor-control#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/ev-hev-vehicles/xev-inverter-inductive-position-sensor-ips#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/infotainment/automotive-cockpit-solution-haptics#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/infotainment/cost-effective-automotive-haptic-touch-key-module-enhanced-driver-safety#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/infotainment/connected-android-based-vehicle-instrument-cluster#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/infotainment/infotainment-automated-driving-systems-fewer-components#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/infotainment/cost-effective-digital-cluster-4-channel-ahl-and-surround-view#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/infotainment/low-cost-digital-instrument-cluster#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/infotainment/full-graphics-cluster-cockpit-solution#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/infotainment/high-end-cockpit-infotainment-solution#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/infotainment/low-cost-tft-instrument-cluster-telematics#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/vehicle-control/advanced-automotive-domain-controller-aadc#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/vehicle-control/high-performance-ev-cooling-system#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/vehicle-control/smart-bicycle-tail-light-alarm-system#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/vehicle-control/solid-state-automotive-power-distribution-module#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/vehicle-control/solid-state-automotive-power-distribution-module-efuse#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/vehicle-control/sunroof-controller#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/vehicle-control/vehicle-control-unit#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/vehicle-control/vehicle-window-control-anti-pinch-safety#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/vehicle-control/zone-ecu-virtualization-solution-platform#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/vehicle-control/automotive-communication-gateway-platform#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/vehicle-control/automotive-monitoring-function-extension#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/vehicle-control/automotive-sensor-canlin-interface#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/vehicle-control/car-telematics-box-module#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/vehicle-control/communication-gateway-integrated-dvrdms-system-solution#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/vehicle-control/connected-gateway-future-ee-architecture#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/vehicle-control/instrument-panel-light-electric-vehicles#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/vehicle-control/tire-pressure-monitoring-system#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/vehicle-control/vehicle-computer-future-ee-architecture#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/vehicle-control/wireless-telematic-unit-vehicle-connectivity#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/vehicle-control/48v-mobility-platform#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/vehicle-control/remote-sensing-inductive-position-sensor-can-lin#winning_combinations_interactive_diagram",
    "https://www.renesas.com/en/applications/automotive/vehicle-control/12v-motor-controller#winning_combinations_interactive_diagram"
]


# Configure Chrome Options
ua = UserAgent()
options = uc.ChromeOptions()
options.add_argument(f"user-agent={ua.random}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

# Initialize Undetected ChromeDriver
driver = uc.Chrome(options=options, headless=True)

# Save directory
SAVE_DIR = "renesas_data"
IMAGE_DIR = os.path.join(SAVE_DIR, "images")
os.makedirs(IMAGE_DIR, exist_ok=True)

def scrape_page(url):
    print(f"Scraping: {url}")
    driver.get(url)

    # Wait for page to load
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(random.uniform(4, 8))
    except:
        print(f"Timeout error: {url}")
        return None

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Extract title
    title_tag = soup.find("h1") or soup.find("h2")
    title = title_tag.text.strip() if title_tag else "Unknown Title"
    print(f"Title Found: {title}")

    # Extract description
    description = "No description available."
    desc_tags = soup.find_all("p")[:3]  # Get first few paragraphs
    if desc_tags:
        description = "\n".join([p.text.strip() for p in desc_tags])

    # Extract SVG Diagram (Only the `<svg>` content)
    svg_container = soup.find("div", class_="diagram-section-media")
    svg_path = None

    if svg_container:
        try:
            svg_tag = svg_container.find("svg")  # Extract only `<svg>` content
            if svg_tag:
                svg_content = str(svg_tag)  # Convert to string
                svg_filename = f"{title.replace(' ', '_')}.svg"
                svg_path = os.path.join(IMAGE_DIR, svg_filename)
                
                # Save cleaned SVG
                with open(svg_path, "w", encoding="utf-8") as svg_file:
                    svg_file.write(svg_content)
                print(f"✅ SVG Diagram Saved: {svg_path}")
            else:
                print("⚠️ No <svg> tag found inside the container.")
        except Exception as e:
            print(f"⚠️ Failed to save SVG diagram: {e}")

    return {"title": title, "description": description, "svg_path": svg_path}

def scrape_all():
    all_designs = []
    
    for url in URLS:
        try:
            design_data = scrape_page(url)
            if design_data:
                all_designs.append(design_data)
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    # Save data to JSON
    json_path = os.path.join(SAVE_DIR, "designs.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_designs, f, indent=4)

    print(f"✅ All data saved to {json_path}")
    driver.quit()

if __name__ == "__main__":
    scrape_all()
