--  @testpoint:函数名称有效值测试，以下划线开头，函数创建成功
drop FUNCTION if EXISTS _func1(integer, integer);
CREATE FUNCTION _func1(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
 /
select proname from pg_proc where proname='_func1';
drop function _func1;