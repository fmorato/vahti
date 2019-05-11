import logging
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

    def print_result(self, string_format="{date:12} {title:40} {price:>6}  {link}"):
        if getattr(self.config, "all", False):
            to_print = self.result
        else:
            to_print = self.new

        for _, item in to_print.items():
            if not item:
                logger.info("No results found")
                return
            print(string_format.format(**item))

    def run_query(self, query):
        result = self.parser.run(query)

        no_db = getattr(self.config, "no-db", False)
        if not no_db:
            new = persist_db(query, result)

        if not no_db and not new:
            logger.info(f"No new items found for {query}")
        if not result:
            logger.info(f"No items found for {query}")

        self._update_result(result)
        self._update_new(new)

    def run_queries(self):
        for query in self.queries:
            logger.debug(f"running {query}")
            self.run_query(query)

    def run(self):
        self.run_queries()
        return 0
