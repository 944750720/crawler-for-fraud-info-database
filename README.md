# Crawler for Fraud Info Database

This is a crawler designed for scraping fraud information from the database of an open-source website.

# Installation of Playwright and BeautifulSoup4

First, open your terminal and run the following commands to install `playwright`, specific browsers, and `BeautifulSoup4`. If you are using Jupyter Notebook, you should use `webkit` instead of `chromium`:

```zsh
pip install playwright
playwright install chromium
pip install BeautifulSoup4
```
Alternatively, if you are using conda like me, you can run the following command to install `BeautifulSoup4`:

```zsh
conda install -c anaconda beautifulsoup4
```
If you are running this on Jupyter Notebook/Colab, you need to download the package for asynchronous running:

```zsh
playwright install-deps
pip install nest_asyncio # asynchronous running package
```
And use `async_main.py` when running.
