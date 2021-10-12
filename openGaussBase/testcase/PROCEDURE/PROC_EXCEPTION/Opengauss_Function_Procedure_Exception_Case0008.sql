-- @testpoint: 验证存储过程是否支持抛出用户自定义异常

create or replace procedure employee_name(ename varchar2)
is
 failure_ename exception;
begin
  if ename<>'smith' then
    raise failure_ename;
    end if;
exception
  when failure_ename then
    raise info 'failure_ename%',ename;
 end;
 /
--调用存储过程
call employee_name('kang');
--清理环境
drop procedure employee_name;