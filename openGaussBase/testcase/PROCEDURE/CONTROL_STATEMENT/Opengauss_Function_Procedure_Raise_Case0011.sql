-- @describe: 存储过程中调试语句  using  MESSAGE

create or replace procedure password_test(passwords number)
is
 failure_password exception;
begin
  if passwords<>'123' then
    raise failure_password;
    end if;
exception
  when failure_password then
    raise 'failure_password:%',passwords using HINT = 'unique_violation';
 end;
 /
 call password_test(234);
 call password_test(123);
 drop procedure password_test;