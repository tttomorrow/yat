--  @testpoint:删除重载函数不带函数参数，合理报错
drop FUNCTION if EXISTS  package_func_overload1(col int, col2  int);
create function  package_func_overload1(col int, col2  int)
RETURNS int
    AS 'select $1 + $2;'
    LANGUAGE SQL
    RETURNS NULL ON NULL INPUT
    package;
/

select proname,propackage from pg_proc where proname='package_func_overload1';
--创建同名函数
drop FUNCTION if EXISTS  package_func_overload1(col int, col2 smallint);
create function  package_func_overload1(col int, col2 smallint)
RETURNS int
    AS 'select $1 + $2;'
    LANGUAGE SQL
    RETURNS NULL ON NULL INPUT
    package;
/
 select proname,propackage from pg_proc where proname='package_func_overload1';
--调用函数
call package_func_overload1(1, 1);
call package_func_overload1(1, 1000);
--删除重载函数不带参数,合理报错
drop function package_func_overload1;
--删除函数带参数
drop FUNCTION package_func_overload1(col int, col2  int);
drop FUNCTION package_func_overload1(col int, col2 smallint);

