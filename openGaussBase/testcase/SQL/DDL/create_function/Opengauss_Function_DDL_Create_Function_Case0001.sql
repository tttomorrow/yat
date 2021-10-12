--  @testpoint:创建函数，不加参数
drop FUNCTION if EXISTS test1();
CREATE FUNCTION test1()returns date AS $$
BEGIN
  return now();
end;
$$ LANGUAGE plpgsql;
/
drop FUNCTION test1();

