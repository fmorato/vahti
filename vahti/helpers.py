import re
import shelve

from vahti.config import SAVE_FILE

MONTH_MAP = {
    "tam": "tammi",
    "hel": "helmi",
    "maa": "maalis",
    "huh": "huhti",
    "tou": "touko",
    "kes": "kesä",
    "hei": "heinä",
    # 'elo': 'elo',
    "syy": "syys",
    "lok": "loka",
    "mar": "marras",
    "jou": "joulu",
}
PATTERN = re.compile(r"\b(" + "|".join(MONTH_MAP.keys()) + r")\b")


def date_parser(date):
    import dateparser

    result = PATTERN.sub(lambda x: MONTH_MAP[x.group()], date)
    return dateparser.parse(result, languages=["fi"])


def new_updated_items(d1, d2):
    """return new and modified items"""
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    modified = {o: d1[o] for o in intersect_keys if d1[o] != d2[o]}
    added = d1_keys - d2_keys
    return modified.update({o: d1[o] for o in added})


def extend_dict(d1, d2):
    """Extends d1 with d2, removing duplicates from d1"""
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    return dict(**{o: d1[o] for o in d1_keys - intersect_keys}, **d2)


def persist_db(query, data):
    with shelve.open(SAVE_FILE, writeback=True) as db:
        saved_query_data = db.get(query)
        if saved_query_data:
            diff = new_updated_items(data, saved_query_data) or {}
            db[query] = dict(**saved_query_data, **diff)
            return diff

        db[query] = data

    return data


def clear_db():
    with shelve.open(SAVE_FILE) as db:
        db.clear()
