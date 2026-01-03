import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

companies = {
    "Infosys": "https://www.infosys.com/",
    "Wipro": "https://www.wipro.com/",
    "TechMahindra": "https://www.techmahindra.com/",
    "HCLTech": "https://www.hcltech.com/",
    "LNT": "https://www.larsentoubro.com/"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

os.makedirs("images", exist_ok=True)
os.makedirs("data", exist_ok=True)

all_data = []

for company, url in companies.items():
    #print(f"\nScraping {company}...")

    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    # Create image folder
    img_dir = os.path.join("images", company)
    os.makedirs(img_dir, exist_ok=True)

    # Title
    title = soup.title.get_text(strip=True) if soup.title else "Not Found"

    # About text (first 3 paragraphs)
    paragraphs = soup.find_all("p")[:3]
    about_text = " ".join(p.get_text(strip=True) for p in paragraphs)

    # Images
    images = soup.find_all("img")
    #print(f"Total images found: {len(images)}")

    downloaded = 0
    blocked = 0

    for img in images:
        if downloaded >= 5:
            break

        src = (
            img.get("src") or
            img.get("data-src") or
            img.get("data-original")
        )

        if not src or src.startswith("data:image"):
            blocked += 1
            continue

        img_url = urljoin(url, src)

        if ".svg" in img_url.lower():
            blocked += 1
            continue

        try:
            r = requests.get(img_url, headers=headers, timeout=15)

            if r.status_code == 200 and "image" in r.headers.get("Content-Type", ""):
                img_name = f"{company}_img_{downloaded+1}.jpg"
                img_path = os.path.join(img_dir, img_name)

                with open(img_path, "wb") as f:
                    f.write(r.content)

                downloaded += 1
                #print(f"Saved image: {img_name}")
            else:
                blocked += 1

        except Exception:
            blocked += 1

    all_data.append({
        "Company": company,
        "Title": title,S
        "About": about_text,
        "Total_Images_Found": len(images),
        "Images_Blocked_or_Skipped": blocked
    })

df = pd.DataFrame(all_data)
df.to_csv("data/companies_data.csv", index=False)

#print(df)