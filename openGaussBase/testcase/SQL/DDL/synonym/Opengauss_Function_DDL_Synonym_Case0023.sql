-- @testpoint: 自定义函数同义词与for loop结合使用
-- @modify at: 2020-11-25
--创建函数
drop function if exists SYN_FUN_008(a int);
create or replace function SYN_FUN_008(a int) return int
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
drop synonym if exists SYN_FUN_SYN_008;
create or replace synonym SYN_FUN_SYN_008 for SYN_FUN_008;
--创建函数
drop function if exists SYN_FUN_005;
create or replace function SYN_FUN_005(a int) return int
as
b int :=0;
begin
	for i in 1..SYN_FUN_SYN_008(a) loop
		b := b + a;
	end loop;
	return b;
end;
/
--调用函数
select SYN_FUN_005(-1);
select SYN_FUN_005(0);
select SYN_FUN_005(1);
select SYN_FUN_005(2);
--清理环境
drop function if exists SYN_FUN_008(a int) cascade;
drop function if exists SYN_FUN_005(a int) cascade;
drop synonym if exists SYN_FUN_SYN_008;