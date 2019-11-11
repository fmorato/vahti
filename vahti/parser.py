import logging
from bs4 import BeautifulSoup
from aiohttp import ClientSession, ClientConnectorError
from vahti.cliargs import arg

logger = logging.getLogger("vahti.parser")

HTML_PARSER = "html.parser"
try:
    import lxml  # pylint: disable=unused-import

    HTML_PARSER = "lxml"
except ImportError:
    pass



@arg.query
class Parser:
    """Base parser to be extended"""

    def __init__(self, params=None, config=None):
        self.url_template = "".format
        self.params = params or {}
        self.config = config or {}
        self.session = None
        self.url = None
        self.last_url = None

    def start(self):
        self.session = ClientSession(
            headers={"User-Agent": "Mozilla/5.0 (X11; Linux i586; rv:62.0) Gecko/20100101 Firefox/62.0"}
        )

    async def close(self):
        await self.session.close()

    def set_query(self, query):
        pass

    async def get(self, url, params=None):
        try:
            async with self.session.get(url, params=params) as response:
                logger.debug(f"queried {response.url} status {response.status}")
                return await response.text()
        except ClientConnectorError as e:
            logger.error(e)
            return None

    def update_url(self, url=None):
        self.url = url or self.url_template(**self.config)

    async def query(self, url=None):
        self.update_url(url)
        logger.debug(f"query {url} with params {self.params}")
        return await self.get(self.url, self.params)

    @staticmethod
    def parse(html):
        logger.debug("parsing html")
        return BeautifulSoup(html, features=HTML_PARSER)

    async def run(self, query, **params):
        self.start()
        self.set_query(query)
        self.params.update(params)
        html = await self.query()
        await self.close()
        if html:
            return self.parse(html)
        else:
            return []
