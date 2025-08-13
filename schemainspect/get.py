from typing import List
from .inspector import NullInspector
from .misc import connection_from_s_or_c
from .pg import PostgreSQL

SUPPORTED = {"postgresql": PostgreSQL}


def get_inspector(x, schema=None, exclude_schemas: List[str] = [], exclude_schema=None):
    if schema and (len(exclude_schemas) > 0 or exclude_schema):
        raise ValueError("Cannot provide both schema and exclude_schema")
    if x is None:
        return NullInspector()

    c = connection_from_s_or_c(x)
    try:
        ic = SUPPORTED[c.dialect.name]
    except KeyError:
        raise NotImplementedError
    except AttributeError:
        ic = SUPPORTED["postgresql"]

    inspected = ic(c)
    if schema:
        inspected.one_schema(schema)
    else:
        all_exclude_schemas = exclude_schemas.copy()
        if exclude_schema:
            all_exclude_schemas.append(exclude_schema)
        for exclude_schema in all_exclude_schemas:
            inspected.exclude_schema(exclude_schema)
    return inspected
