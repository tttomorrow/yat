-- @testpoint: lower函数作为定义函数的返回值
drop function if exists f_lower;
create or replace function f_lower(A char)
return char
as
begin
    return lower(A);
end;
/
select f_lower('LLKJaJKKaQ');
drop function if exists f_lower;