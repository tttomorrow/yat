-- @testpoint: 获取参数列表来确定一个函数

select pg_get_function_identity_arguments(a.oid) from PG_PROC a where a.proname = 'age' order by a.oid desc;
select pg_get_function_identity_arguments(a.oid) from PG_PROC a where a.proname = 'to_char' order by a.oid desc;
select pg_get_function_identity_arguments(a.oid) from PG_PROC a where a.proname = 'pg_get_function_identity_arguments' order by a.oid desc;
select pg_get_function_identity_arguments(a.oid) from PG_PROC a where a.proname = 'array_cat' order by a.oid desc;