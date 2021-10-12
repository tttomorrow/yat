-- @testpoint: 验证存储过程是否支持抛出用户自定义异常 low_hiredate

create or replace procedure employee_hiredate(hiredate varchar2)
is 
 low_hiredate exception;
begin
  if hiredate>to_date('1981-04-02','yyyy-mm-dd') then
    raise low_hiredate;
    end if;
exception
  when low_hiredate then
    raise info 'low_hiredate:%',hiredate;
 end;
 /
call employee_hiredate(to_date('2018-09-12','yyyy-mm-dd'));
drop procedure employee_hiredate;