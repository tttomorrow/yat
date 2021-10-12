-- @testpoint: pg_get_functiondef函数获取函数的定义
select pg_get_functiondef(oid) from PG_PROC where proname = 'age';