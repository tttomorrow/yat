-- @testpoint: left函数作为自定义函数的返回值
drop function if exists test_left;
create or replace function test_left(a varchar2) return varchar2
is
begin
return left(a,4);
end;
/
select test_left('xiexiaoytu');
drop function if exists test_left;