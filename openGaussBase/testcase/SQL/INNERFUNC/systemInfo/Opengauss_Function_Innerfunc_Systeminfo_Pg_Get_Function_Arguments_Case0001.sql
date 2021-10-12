-- @testpoint: 获取函数定义的参数列表（带默认值）
select pg_get_function_arguments(oid) from PG_PROC where proname = 'age';