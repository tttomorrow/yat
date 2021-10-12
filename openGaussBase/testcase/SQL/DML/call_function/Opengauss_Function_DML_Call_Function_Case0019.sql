-- @testpoint: 调用函数，对于非重载的函数，参数列表不包含出参，合理报错
drop FUNCTION if EXISTS func_increment_sql002(num1 IN integer, num2 IN integer, res OUT integer);
--创建带出参的函数
CREATE FUNCTION func_increment_sql002(num1 IN integer, num2 IN integer, res OUT integer )
RETURN integer
AS
BEGIN
res := num1 + num2;
END;
/
select proname from pg_proc where proname='func_increment_sql002';
--入参传入常量，出参不传值，合理报错
CALL func_increment_sql002(1,2);
drop FUNCTION func_increment_sql002;