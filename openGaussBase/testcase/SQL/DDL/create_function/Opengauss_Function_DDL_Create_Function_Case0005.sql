--  @testpoint:指定REPLACE，返回参数类型变化，不会替换原有函数，新建函数合理报错
--预置条件，创建函数
drop function if exists func_add_sql(integer, integer);
CREATE FUNCTION func_add_sql(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/
select proname from pg_proc where proname='func_add_sql';


--指定REPLACE，返回参数类型变化，不会替换原有函数，新建函数合理报错
CREATE or replace FUNCTION func_add_sql(integer, integer) RETURNS bigint
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
 /
drop function func_add_sql(integer, integer);