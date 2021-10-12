-- @testpoint: 匿名块定义 验证匿名块是否支持end if，IF ELSIF ELSE 连用

DECLARE
  grade CHAR(1);
BEGIN
  grade := 'B';
  IF grade = 'A' THEN
    raise info 'Excellent';
  ELSIF grade = 'B' THEN
    raise info 'Very Good';
  ELSIF grade = 'C' THEN
    raise info 'Good';
  ELSIF grade = 'D' THEN
    raise info 'Fair';
  ELSIF grade = 'F' THEN
    raise info 'Poor';
  ELSE
    raise info 'No such grade';
  END IF;
END;
/
