select *
from (
select
    coalesce(
        n.nspname,
        case when l.objtype = 'schema' then l.objname end,
        ''
    ) as "schema",
    case
        when l.objtype = 'table column' then 'column'
        else l.objtype
    end as object_type,
    l.objname as object_identity,
    l.provider,
    l.label
from pg_catalog.pg_seclabels l
left join pg_catalog.pg_namespace n on n.oid = l.objnamespace
where l.objtype in (
    'aggregate',
    'domain',
    'foreign table',
    'function',
    'materialized view',
    'procedure',
    'routine',
    'schema',
    'sequence',
    'table',
    'table column',
    'type',
    'view'
)
-- SKIP_INTERNAL and coalesce(n.nspname, case when l.objtype = 'schema' then l.objname end, '') not in ('pg_catalog','information_schema')
-- SKIP_INTERNAL and coalesce(n.nspname, case when l.objtype = 'schema' then l.objname end, '') not like 'pg_temp_%'
-- SKIP_INTERNAL and coalesce(n.nspname, case when l.objtype = 'schema' then l.objname end, '') not like 'pg_toast_temp_%'

union all

select
    '' as "schema",
    'role' as object_type,
    pg_catalog.quote_ident(r.rolname) as object_identity,
    l.provider,
    l.label
from pg_catalog.pg_shseclabel l
join pg_catalog.pg_authid r on r.oid = l.objoid
where l.classoid = 'pg_catalog.pg_authid'::pg_catalog.regclass
-- SKIP_INTERNAL and r.rolsuper = false
-- SKIP_INTERNAL and r.rolname not like 'pg_%'
) labels
order by "schema", object_type, object_identity, provider;
