--  @testpoint:函数参数名无效值测试，以数字开头，合理报错



CREATE FUNCTION test_func3(1_$ integer, 2_$integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/