-- @testpoint: 15.创建与系统函数char()相同名字的自定义函数,分别加用户名与不加用户名调用
drop user if exists self_func_042 CASCADE;
create user self_func_042 identified by 'Xiaxia@123';
create or replace function self_func_042.add_months( x int )
return int
as
begin
    return 520;
end;
/
select add_months('2019-03-01',1) from sys_dummy;
select self_func_042.add_months(11) from sys_dummy;
drop user self_func_042 cascade;
