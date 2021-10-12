--  @testpoint:指定REPLACE，参数类型变化，不会替换原有函数，而是会建立新的函数
--预置条件，创建函数
drop function if exists func_add_sql2(integer, integer);
CREATE FUNCTION func_add_sql2(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/



--指定REPLACE，参数类型变化，不会替换原有函数，而是会建立新的同名函数
CREATE or replace FUNCTION func_add_sql2(bigint, bigint) RETURNS bigint
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/
--存在两个同名的func_add_sql2函数
select proname proargnames,proargtypes,proallargtypes,prosrc from pg_proc where proname='func_add_sql2';
drop function func_add_sql2(integer, integer);
drop function func_add_sql2 (bigint, bigint);