-- @testpoint: 创建与系统函数strpos相同名字的自定义函数并调用

drop schema if exists self_func cascade;
create schema self_func;
create or replace function self_func.strpos( x int )
return int
as
begin
    return 20201231;
end;
/

select self_func.strpos(1);

drop function self_func.strpos;
drop schema self_func cascade;