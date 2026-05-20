from sqlbag import S

from schemainspect import get_inspector
from schemainspect.pg.obj import InspectedRule


def test_rule_statements():
    rule = InspectedRule(
        name="protect_accounts",
        schema="public",
        table_name="accounts",
        enabled="O",
        full_definition=(
            "CREATE RULE protect_accounts AS\n"
            "    ON UPDATE TO public.accounts DO INSTEAD NOTHING"
        ),
    )

    assert (
        rule.drop_statement
        == 'drop rule if exists "protect_accounts" on "public"."accounts";'
    )
    assert rule.create_statement.endswith("NOTHING;")

    rule.enabled = "D"
    assert (
        rule.create_statement.splitlines()[-1]
        == 'ALTER TABLE "public"."accounts" DISABLE RULE "protect_accounts";'
    )


def test_rules(db):
    with S(db) as s:
        s.execute(
            """
CREATE TABLE accounts (id integer, manager text, secret text);
CREATE VIEW safe_accounts AS SELECT id, manager FROM accounts;
CREATE RULE protect_accounts AS
    ON UPDATE TO accounts
    WHERE old.manager <> current_user
    DO INSTEAD NOTHING;
        """
        )

        i = get_inspector(s)

        assert '"public"."safe_accounts"."_RETURN"' not in i.rules

        rule = i.rules['"public"."accounts"."protect_accounts"']
        assert rule.name == "protect_accounts"
        assert rule.schema == "public"
        assert rule.table_name == "accounts"
        assert rule.enabled == "O"
        assert "CREATE RULE protect_accounts AS" in rule.create_statement
        assert "ON UPDATE TO public.accounts" in rule.create_statement
        assert "DO INSTEAD NOTHING" in rule.create_statement
        assert (
            rule.drop_statement
            == 'drop rule if exists "protect_accounts" on "public"."accounts";'
        )

        s.execute(rule.drop_statement)
        s.execute(rule.create_statement)

        i = get_inspector(s)
        assert '"public"."accounts"."protect_accounts"' in i.rules
