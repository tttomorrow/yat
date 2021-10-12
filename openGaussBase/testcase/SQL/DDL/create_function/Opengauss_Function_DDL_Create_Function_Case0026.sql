--  @testpoint:函数参数名无效值测试，参数名为空字符串，合理报错
CREATE FUNCTION t_func7('' integer, '' integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/