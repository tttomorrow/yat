-- @testpoint: 函数内部设置current_schema，执行完函数前后current_schema不变
--查询当前schema，默认是public
select current_schema;
--创建schema
drop schema if exists sc;
create schema sc;
--创建函数set current_schema
drop FUNCTION if EXISTS func_add_sql(integer, integer);
--创建函数
    CREATE FUNCTION func_add_sql(integer, integer) RETURNS integer
   as 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT
    set current_schema=sc;
    /
--查询current_schema不变
select current_schema;
drop FUNCTION func_add_sql(integer, integer);

--函数内部设置search_path，执行完函数前后search_path不变
--执行如下命令查看搜索路径
SHOW SEARCH_PATH;
--创建函数set search_path
drop FUNCTION if EXISTS func_add_sql(integer, integer);
--创建函数
    CREATE FUNCTION func_add_sql(integer, integer) RETURNS integer
   as 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT
    set search_path=myschema, public;
    /
    --查询search_path不变
SHOW SEARCH_PATH;
drop FUNCTION func_add_sql(integer, integer);
drop schema sc;