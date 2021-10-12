--  @testpoint:修改函数的package属性为非package属性，合理报错
drop FUNCTION if EXISTS  package_func_overload5;
--创建函数，修改package属性为not package
create function  package_func_overload5(col int, col2  int)
RETURNS int
    AS 'select $1 + $2;'
    LANGUAGE SQL
    RETURNS NULL ON NULL INPUT
    not package;
    /