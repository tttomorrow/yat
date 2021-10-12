--  @testpoint:删除重载函数带函数参数，删除成功
drop FUNCTION if EXISTS  package_func_overload;
create function  package_func_overload(col int, col2  int)
RETURNS int
    AS 'select $1 + $2;'
    LANGUAGE SQL
    RETURNS NULL ON NULL INPUT
    package;
/

select proname,propackage from pg_proc where proname='package_func_overload';
--创建同名函数
create function  package_func_overload(col int, col2 smallint)
RETURNS int
    AS 'select $1 + $2;'
    LANGUAGE SQL
    RETURNS NULL ON NULL INPUT
    package;
/
 select proname,propackage from pg_proc where proname='package_func_overload';
--调用函数
 call package_func_overload(1, 1);
call package_func_overload(1, 1000);
--删除重载函数带参数
drop function package_func_overload(col int, col2 smallint) ;
drop function package_func_overload(col int, col2  int);