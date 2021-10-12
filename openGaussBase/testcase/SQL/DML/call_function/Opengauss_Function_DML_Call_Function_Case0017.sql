-- @testpoint: 参数列表中仅出现参数值,参数值的排列顺序和函数定义时不一致，合理报错
drop FUNCTION if EXISTS func_add_sql018;
CREATE FUNCTION func_add_sql018(num1 integer, num2 char) RETURN INTEGER
AS
BEGIN
RETURN (num1,num2);
END;
/
--调用函数，参数顺序和定义函数时不一致
CALL func_add_sql018('hello',99);
drop FUNCTION func_add_sql018;