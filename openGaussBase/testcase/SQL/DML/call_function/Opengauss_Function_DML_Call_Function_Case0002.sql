-- @testpoint: 带schema，按参数值传递,调用函数（schema已存在）
drop SCHEMA if EXISTS hs;
CREATE SCHEMA hs;
drop FUNCTION if EXISTS hs.func_add_sql002;
CREATE FUNCTION hs.func_add_sql002(num1 integer, num2 integer) RETURN integer
AS
BEGIN
RETURN num1 + num2;
END;
/

CALL hs.func_add_sql002(1, 3);
drop FUNCTION hs.func_add_sql002;
drop schema hs;