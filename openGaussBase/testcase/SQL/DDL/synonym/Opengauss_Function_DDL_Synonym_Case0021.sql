-- @testpoint: 自定义函数同义词与if结合使用
-- @modify at: 2020-11-25
--自定义函数
drop function if exists SYN_FUN_021;
create or replace function SYN_FUN_021(c bigint) return int
as
  b int := c;
begin
	for i in 1..3 loop
		b := b + c;
	end loop;
	return b;
end;
/
--建自定义函数同义词
drop synonym if exists SYN_FUN_SYN_021;
create or replace synonym SYN_FUN_SYN_021 for SYN_FUN_021;
--创建函数
drop function if exists SYN_FUN_005 ;
create or replace function SYN_FUN_005(e int) return int
as
e int;
d int :=0;
begin
	if SYN_FUN_SYN_021(e)<0 then
		d := 1;
	elseif SYN_FUN_SYN_021(e)=0 then
		d := 2;
	else
		d := 3;
	end if;
	return d;
end;
/
--调用函数
select SYN_FUN_005(-1);
select SYN_FUN_005(0);
select SYN_FUN_005(2);
--清理环境
drop function if exists SYN_FUN_021;
drop function if exists SYN_FUN_005;
drop synonym if exists SYN_FUN_SYN_021;