# 🏴‍☠️ Pirate Bay Magnet Scraper

A simple Python script to scrape and extract magnet links from Pirate Bay search result pages — no API required.

## 🔧 Features

* Parses Pirate Bay search result pages directly from a full URL.
* Extracts all magnet links from the given results.
* Supports `--url` command-line argument to scrape any Pirate Bay search.

## 📦 Requirements

* Python 3.7+
* `requests`
* `beautifulsoup4`

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🚀 Usage

```bash
python main.py --url "<full search URL>"
```

### Example

```bash
python main.py --url "https://thepiratebay.org/search.php?q=enen+HEVC&cat=0"
```

### Output

Magnet links will be printed to the console:

```
magnet:?xt=urn:btih:ABC123...&dn=Some+Torrent+Name&tr=...
magnet:?xt=urn:btih:XYZ456...&dn=Another+Torrent+Name&tr=...
```

## 📄 Example Output with Torrent Titles

```bash
Torrent: Enen no Shouboutai S02E01 HEVC
Magnet: magnet:?xt=urn:btih:ABC123&dn=Enen+no+Shouboutai...&tr=...

Torrent: Enen no Shouboutai Movie HEVC
Magnet: magnet:?xt=urn:btih:XYZ456&dn=Enen+no+Shouboutai+Movie...&tr=...
```

## 🛡️ Disclaimer

This tool is provided for educational purposes only. Make sure you comply with your country's laws and Pirate Bay's terms of service.

## 📁 Project Structure

```
PirateBayScraper/
├── main.py              # Entry point script
├── requirements.txt     # Python dependencies
└── README.md            # This file
```
