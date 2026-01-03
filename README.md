# Company Website Web Scraper

This project scrapes official company websites to extract:
- Website title
- About section (first 3 paragraphs)
- Image statistics (found, downloaded, blocked)

Images are downloaded locally and metadata is stored in a CSV file.

## Image Download Details

- For each company website, up to **5 images** are downloaded.
- Images are saved locally in the following structure:

  images/
  ├── Infosys/
  ├── Wipro/
  ├── TechMahindra/
  ├── HCLTech/
  └── LNT/

- SVG and base64 images are skipped.
- Images are downloaded only if the response content type is valid.
- The `images/` directory is excluded from version control using `.gitignore`.


## Technologies Used
- Python
- Requests
- BeautifulSoup
- Pandas

## Output
- `data/companies_data.csv`
- `images/` (local only, ignored in GitHub)

## How to Run
```bash
pip install requests beautifulsoup4 pandas
python scraper.py
