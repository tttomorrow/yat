--  @testpoint:创建函数时指定参数数据类型是integer，返回数据类型是别名int4，函数创建成功
--预置条件，创建函数
drop function if exists func_add_sql(integer, integer);
CREATE FUNCTION func_add_sql(integer, integer) RETURNS int4
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
 /
select proname proargnames,proargtypes,proallargtypes,prosrc,prorettype from pg_proc where proname='func_add_sql';
drop function func_add_sql(integer, integer);

