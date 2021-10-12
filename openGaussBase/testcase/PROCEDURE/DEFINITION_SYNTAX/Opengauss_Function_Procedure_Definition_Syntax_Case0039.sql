-- @testpoint: 匿名块定义 验证匿名块是否支持end if,if else


DECLARE
x NUMBER(3) := 10;
BEGIN
IF x < 10 THEN
raise info 'X is less than 10';
ELSE
raise info 'X is not less than 10';
END IF;
END;
/
