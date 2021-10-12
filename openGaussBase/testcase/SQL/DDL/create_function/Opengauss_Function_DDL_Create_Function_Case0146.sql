--  @testpoint:设置数据库的会话参数值为RESET，使用=
drop FUNCTION if EXISTS func_add_sql(integer, integer);
--创建函数
    CREATE FUNCTION func_add_sql(integer, integer) RETURNS integer
   as 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT
    set current_schema=RESET;
    /
    call func_add_sql(99,0);

    drop function func_add_sql(integer, integer);