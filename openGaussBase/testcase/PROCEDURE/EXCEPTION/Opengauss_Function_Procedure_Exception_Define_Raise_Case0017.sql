-- @testpoint: 验证是否支持匿名块抛出自定义异常 failure_num

declare 
i number:=9;
failure_num exception;
begin 
if i=9 then
raise failure_num;
end if; 
exception 
when failure_num then
raise info ':%',SQLERRM;
end;
/
