-- @testpoint: 自定义函数同义词在其他自定义函数中使用中调用
--创建函数
drop function if exists fun_027_01(a int) cascade;
create or replace function fun_027_01(a int) return int
as
b int:= a;
begin
	for i in 1..a loop
		b:=b+1;
	end loop;
	return b;
end;
/
--创建同义词
drop synonym if exists syn_fun_027_01;
create synonym syn_fun_027_01 for fun_027_01;
--创建函数
create or replace function fun_027_02(a int) return int
as
b int:= a;
begin
    return syn_fun_027_01(a);
end;
/
--创建同义词
drop synonym if exists syn_fun_027_02;
create synonym syn_fun_027_02 for fun_027_02;
--调用函数
select syn_fun_027_02(3);
--清理环境
drop function if exists fun_027_01(a int) cascade;
drop synonym if exists syn_fun_027_01;
drop function fun_027_02(a int);
drop synonym if exists syn_fun_027_02;


