--  @testpoint:函数名称无效值测试，以数字开头，合理报错
CREATE FUNCTION 1_func1(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/