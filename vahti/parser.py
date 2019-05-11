import logging
import requests
from bs4 import BeautifulSoup
from vahti.cliargs import arg

logger = logging.getLogger("vahti.parser")


@arg.query
class Parser:
    """Base parser to be extended"""

    def __init__(self, params=None, config=None):
        self.url_template = "".format
        self.params = params or {}
        self.config = config or {}
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux i586; rv:62.0) Gecko/20100101 Firefox/62.0"})
        self.last_url = ""

    def set_query(self, query):
        pass

    def query(self, url=""):
        url = url or self.url_template(**self.config)
        logger.debug(f"query {url} with params {self.params}")
        r = requests.get(url, params=self.params)
        self.last_url = r.url
        logger.debug(f"queried {r.url} status {r.status_code}")

        return r.text

    @staticmethod
    def parse(html):
        logger.debug("parsing html")
        return BeautifulSoup(html, features="html.parser")

    def run(self, query, **params):
        self.set_query(query)
        self.params.update(params)
        html = self.query()
        return self.parse(html)
