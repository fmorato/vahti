import logging
import asyncio
from vahti.helpers import extend_dict, persist_db

logger = logging.getLogger("vahti")

# TODO: write tests
# TODO: create a config file and write logs somewhere


class Vahti:
    def __init__(self, parser=None, queries=None, config=None):
        self.parser = parser
        self.config = config
        self.queries = queries
        self.result = {}
        self.new = {}

    def _update_result(self, result):
        if result:
            self.result = extend_dict(self.result, result)

    def _update_new(self, new):
        if new:
            self.new = extend_dict(self.new, new)

    def print_result(self, string_format="{date:12} {title:40} {price:>6}  {link}".format):
        if self.config["all"] or self.config["no_db"]:
            to_print = self.result
        else:
            to_print = self.new

        if not to_print:
            logger.info("No results to print")
            return

        string_format = self.parser.item_format or string_format
        for _, item in to_print.items():
            print(string_format(**item))

    async def run_query(self, query):
        result = await self.parser.run(query)
        new = {}
        no_db = self.config["no_db"]
        if not no_db:
            new = persist_db(query, result)

        if not no_db and not new:
            logger.info(f"No new items found for {query}")
        if not result:
            logger.info(f"No items found for {query}")

        self._update_result(result)
        self._update_new(new)

    async def run_queries(self):
        # https://stackoverflow.com/questions/49118449/python-3-6-async-get-requests-in-with-aiohttp-are-running-synchronously
        requests = []
        for query in self.queries:
            logger.debug(f"running {query}")
            requests.append(self.run_query(query))

        await asyncio.gather(*requests)

    def run(self):
        loop = asyncio.get_event_loop()
        if self.queries:
            loop.run_until_complete(self.run_queries())
        else:
            loop.run_until_complete(self.run_query(""))
        return 0
