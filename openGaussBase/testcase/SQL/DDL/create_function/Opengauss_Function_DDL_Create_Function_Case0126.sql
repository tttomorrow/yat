--  @testpoint:package函数和非package函数进行重载，合理报错
 drop FUNCTION if EXISTS  package_func_overload4;
--创建重载函数
create function  package_func_overload4(col int, col2  int)
RETURNS int
    AS 'select $1 + $2;'
    LANGUAGE SQL
    RETURNS NULL ON NULL INPUT
    package;
    /
    select proname from pg_proc where proname='package_func_overload4';
--创建非package函数重载package函数，合理报错
create function  package_func_overload4(col int, col2  smallint)
RETURNS int
    AS 'select $1 + $2;'
    LANGUAGE SQL
    RETURNS NULL ON NULL INPUT;
/
  drop FUNCTION   package_func_overload4;