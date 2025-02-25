# Web scrapper for fedreserve speeches

## Installation
Use python's pip to install information
```bash
pip install -r requirements.txt
```

## Usage
Usage with python3
```bash
python main.py
```

Inside the file the speecher to be download for can be specified:
```bash
if __name__ == '__main__':
    speeches = TestGetPowellsLinks()
    options = SeleniumOptions(browser="firefox", headless=True, speaker="jefferson")
    speeches.setup_method(options)
    speeches.run()
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

TODO: test other/former. Not tested

Is possible to make a loop and iterate through each of the users if desirable. Data will be downloaded in data/
