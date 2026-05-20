with extension_oids as (
  select
      objid
  from
      pg_depend d
  where
      d.refclassid = 'pg_extension'::regclass
      and d.classid = 'pg_rewrite'::regclass
)
select
    rw.rulename as "name",
    nsp.nspname as "schema",
    cls.relname as table_name,
    rw.ev_enabled as enabled,
    pg_get_ruledef(rw.oid) as full_definition,
    rw.oid in (select * from extension_oids) as extension_owned
from pg_rewrite rw
join pg_class cls on cls.oid = rw.ev_class
join pg_namespace nsp on nsp.oid = cls.relnamespace
where rw.rulename != '_RETURN'
-- SKIP_INTERNAL and not rw.oid in (select * from extension_oids)
order by schema, table_name, name;
