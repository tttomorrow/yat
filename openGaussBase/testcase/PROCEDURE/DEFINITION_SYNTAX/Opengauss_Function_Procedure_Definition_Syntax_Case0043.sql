-- @testpoint: 匿名块定义 验证匿名块是否支持end if

DECLARE
  sales  NUMBER(8,2) := 20000;
  bonus  NUMBER(6,2);
BEGIN
   IF sales > 50000 THEN
      bonus := 1500;
   ELSIF sales > 35000 THEN
      bonus := 500;
   ELSE
      bonus := 100;
   END IF;
END;
/
