-- @testpoint: 验证存储过程是否支持抛出用户自定义异常 failure_username

create or replace procedure user_test(username varchar2)
is 
 failure_username exception;
begin
  if username<>'wangkang' then
    raise failure_username;
    end if;
exception
  when failure_username then
    raise info 'failure_username:%',username;
 end;
 /
 call user_test('kang');
drop procedure user_test;