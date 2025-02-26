# Web scrapper for fedreserve speeches

## Installation
Use python's pip to install information
```bash
pip install -r requirements.txt
```

## Usage
To use this scrapper just import it with the specified options and use the .run() method. By default it will create a directory /data on the current folder, in which it will download a .txt of the speeches from a specific actor.

Options:
```python
from federal_scrapper import FederalScrapper
federal_scrapper = FederalScrapper(browser="firefox", headless=False, speaker="powell", debug=False, download_dir="path")
federal_scrapper.run()
```

Possible speakers:
```bash
{
    "powell",
    "jefferson",
    "barr",
    "bowman",
    "cook",
    "kugler",
    "waller",
    "former",
    "other"
}
```
