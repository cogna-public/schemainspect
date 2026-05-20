from schemainspect.pg.obj import InspectedSecurityLabel, SECURITY_LABELS_QUERY


def test_security_label_statements():
    label = InspectedSecurityLabel(
        schema="public",
        object_type="table",
        object_identity="public.accounts",
        provider="selinux",
        label="system_u:object_r:sepgsql_table_t:s0",
    )

    assert (
        label.create_statement
        == 'security label for "selinux" on table public.accounts '
        "is 'system_u:object_r:sepgsql_table_t:s0';"
    )
    assert (
        label.drop_statement
        == 'security label for "selinux" on table public.accounts is null;'
    )


def test_security_label_escapes_label_literals():
    label = InspectedSecurityLabel(
        schema="public",
        object_type="column",
        object_identity="public.accounts.manager",
        provider="selinux",
        label="manager's label",
    )

    assert label.create_statement.endswith("is 'manager''s label';")


def test_role_security_label_statements():
    label = InspectedSecurityLabel(
        schema="",
        object_type="role",
        object_identity='"app-user"',
        provider="selinux",
        label="system_u:object_r:sepgsql_role_t:s0",
    )

    assert (
        label.create_statement
        == 'security label for "selinux" on role "app-user" '
        "is 'system_u:object_r:sepgsql_role_t:s0';"
    )
    assert (
        label.drop_statement
        == 'security label for "selinux" on role "app-user" is null;'
    )


def test_security_label_query_includes_shared_role_labels():
    assert "pg_catalog.pg_shseclabel" in SECURITY_LABELS_QUERY
    assert "'role' as object_type" in SECURITY_LABELS_QUERY
    assert "pg_catalog.pg_authid" in SECURITY_LABELS_QUERY
