--  @testpoint:package函数和非package函数进行替换，合理报错
drop FUNCTION if EXISTS  package_func_overload3;
--创建重载函数
create function  package_func_overload3(col int, col2  int)
RETURNS int
    AS 'select $1 + $2;'
    LANGUAGE SQL
    RETURNS NULL ON NULL INPUT
    package;
    /
    select proname from pg_proc where proname='package_func_overload3';

  --使用replace替换重载函数为非重载函数，合理报错
create or replace function  package_func_overload3(col int, col2  smallint)
RETURNS int
    AS 'select $1 + $2;'
    LANGUAGE SQL
    RETURNS NULL ON NULL INPUT;
    /
 drop FUNCTION package_func_overload3;