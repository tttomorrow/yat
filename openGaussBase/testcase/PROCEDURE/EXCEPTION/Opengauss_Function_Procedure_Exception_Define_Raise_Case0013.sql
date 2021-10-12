-- @testpoint: 验证存储过程是否支持抛出用户自定义异常 failure_number

create or replace procedure number_test(tests number)
is 
 failure_number exception;
begin
  if tests<0 then
    raise failure_number;
    end if;
exception
  when failure_number then
    raise info 'failure_number:%',tests;
 end;
 /
 call number_test(-9);
drop procedure number_test;