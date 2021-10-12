-- @testpoint: 验证是否支持存储过程抛出自定义异常的错误码

create or replace  procedure  exception_016 ()  as
declare
i number:=0;
failure_num exception;
begin
if i=0 then
raise failure_num;
end if;
exception
when failure_num then
raise info ':%',sqlerrm;
end;
/
--调用存储过程
call exception_016();
--清理环境
drop procedure exception_016;