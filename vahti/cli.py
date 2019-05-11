import argparse
import sys
import logging

from vahti import Vahti, parsers
from vahti.helpers import clear_db
from vahti.parsers.cliargs import ARG_LIST_PROP

# TODO: make persistance optional

logger = logging.getLogger("vahti.cli")


class VahtiCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="vahti")
        self.parser.add_argument("-a", "--all", action="store_true", help="display all results")
        self.parser.add_argument("--clear", action="store_true", help="clear the database and exit")
        self.parser.add_argument("--no-db", action="store_true", help="don't persist")
        self.subparsers = self.parser.add_subparsers(dest="parser", title="parser")

        for parser, parser_class in parsers.avaliable_parsers.items():
            p = self.subparsers.add_parser(parser, help=parser_class.__doc__)
            for arg in getattr(parser_class, ARG_LIST_PROP, []):
                p.add_argument(*arg[0], **arg[1])

        self.args = None

    def run_parser(self, args=None):
        # logger.debug(vars(self.args))
        if getattr(self.args, "clear", False):
            logger.debug("clearing db")
            clear_db()
            return 0

        parser = getattr(self.args, "parser", None)
        if not parser:
            self.parser.parse_args(args + ["--help"])
            return 1

        logger.debug("running %s parser", parser)

        config = vars(self.args)
        vahti = Vahti(config)
        vahti.parser = parsers.avaliable_parsers[parser](config=config)
        vahti.queries = getattr(self.args, "query", [])
        vahti.run()

        return 0

    def run(self, args=None):
        args = args or sys.argv[1:]
        if not args:
            args = ["--help"]
        self.args = self.parser.parse_args(args=args)
        try:
            return self.run_parser(args)
        except KeyboardInterrupt:
            logger.error("*** terminated by keyboard ***")
            return 2

    def main(self):
        logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s %(name)s %(message)s")
        logging.getLogger("requests").setLevel(logging.WARNING)

        sys.exit(self.run())
