-- @testpoint: log函数在匿名块中用于定义变量
declare
LOG_002 numeric;
begin
LOG_002:= 10;
raise info':%',(log(LOG_002,100.0));
end;
/