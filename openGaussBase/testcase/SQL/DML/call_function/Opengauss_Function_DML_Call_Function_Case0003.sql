--  @testpoint:带schema，按参数值传递,调用函数（schema不存在，合理报错）
drop FUNCTION if EXISTS func_add_sql003;
CREATE FUNCTION func_add_sql003(num1 integer, num2 integer) RETURN integer
AS
BEGIN
RETURN num1 + num2;
END;
/

CALL hxs.func_add_sql002(1, 3);
drop FUNCTION func_add_sql003;