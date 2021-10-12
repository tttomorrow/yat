-- @testpoint: mod函数用于自定义函数返回值
drop function if exists dd_mod;
create or replace function dd_mod() return number
is
begin
return mod('434234',454);
end;
/
select dd_mod();
drop function if exists dd_mod;