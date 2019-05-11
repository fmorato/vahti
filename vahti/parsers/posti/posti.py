import logging

from vahti.parser import Parser

logger = logging.getLogger("vahti.posti")


class Posti(Parser):
    """A parser for posti.fi"""

    def __init__(self, query=""):
        super().__init__()
        self.url_template = "https://www.posti.fi/itemtracking/posti/search_by_shipment_id"
        self.params = {"lang": "fi", "ShipmentId": query}

    def parse(self, html):
        soup = super().parse(html)
        items = soup.find_all("div", attrs={"id": "shipment-event-table-cell"})

        result = {}

        # TODO: use a list and setup proper diff checking in persistent
        for item in items:
            result[item.find("div").text] = None

        return result

    def set_query(self, query=""):
        self.params["ShipmentId"] = query
