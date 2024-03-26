# use the scrapy venv
```
python3 -m venv ~/tools/venvs/scrapy-test

source ~/tools/venvs/scrapy-test/bin/activate
pip install Scrapy
pip install beautifulsoup4
```
# pip install eyeD3 for mp3 id3 tag
# Change the cookie in constants.py
# do crawl
```
scrapy crawl zhihu
scrapy crawl lianjia_chengjiao
```
OR
```
scrapy crawl lianjia
```

to launch in vscode, add the following launch.json:
```
{
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "module": "scrapy",
            "args": [
                "crawl",
                "lianjia"
            ],
            "console": "internalConsole"
        }
    ]
}
```
