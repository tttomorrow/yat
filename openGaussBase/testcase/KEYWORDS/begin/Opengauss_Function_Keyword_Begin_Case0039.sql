-- @testpoint: 用在存储过程中

create or replace function test_too_many_error return int is
v1 int;
v2 int;
begin
v1 = 0;
v2 = v1;
v2 = v1;
v2 = v1;
v2 = v1;
v2 = v1;
v2 = v1;
v2 = v1;
v2 = v1;
v2 = v1;
v2 = v1;
v2 = v1;
v2 = v1;
v2 = v1;
v2 = v1;
v2 = v1;
v2 = v1;
v2 = v1;
v2 = v1;
return v1;
end;
/

begin
execute immediate 'select test_too_many_error() from sys_dummy';
end;
/
drop function test_too_many_error;