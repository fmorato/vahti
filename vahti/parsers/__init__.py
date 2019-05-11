import sys
import inspect
import importlib
import pkgutil

modules = []
for _, name, is_pkg in pkgutil.walk_packages(__path__):
    if is_pkg:
        modules.append(importlib.import_module(__name__ + "." + name))

result = {}
for module in modules:
    result.update(dict(inspect.getmembers(sys.modules[module.__name__], inspect.isclass)))

available_parsers = result

# so we can do "from vahti.parsers import ParserClass"
# Is there a better way of doing this?
__all__ = []
for parser, klass in zip(modules, result):
    __all__.append(klass)
    exec(f"from {parser.__name__} import {klass}", locals())  # pylint: disable=exec-used

# TODO: move parsers out of vahti
