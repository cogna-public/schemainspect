import uuid

from schemainspect import get_inspector
from sqlbag import S, temporary_database


def test_load_roles_keeps_non_internal_pga_role():
    rolename = "pganon_dumper_{}".format(uuid.uuid4().hex[:8])

    with temporary_database(host="localhost") as dburl:
        with S(dburl) as s:
            s.execute(f"create role {rolename};")

            try:
                inspector = get_inspector(s)
                inspector.load_roles()

                assert rolename in inspector.roles
            finally:
                s.execute(f"drop role if exists {rolename};")
