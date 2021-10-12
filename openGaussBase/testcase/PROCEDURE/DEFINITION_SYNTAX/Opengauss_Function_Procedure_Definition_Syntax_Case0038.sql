-- @testpoint: 匿名块定义 验证匿名块是否支持end if

declare
  x number(3):=9;
begin
if x<10 then
raise info 'x is less than10';
end if;
end;
/




