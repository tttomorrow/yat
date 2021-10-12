-- @testpoint: 自定义函数同义词作为入参与avg函数结合使用
--建自定义函数
drop function if exists SYN_FUN_010_001(c int) cascade;
create or replace function SYN_FUN_010_001(c int)return number
as
b int := c;
begin
	for i in 1..c loop
		b:= b - 1;
	end loop;
	return b;
end;
/
--建自定义函数同义词
drop synonym if exists SYN_FUN_SYN_010_001;
create or replace synonym SYN_FUN_SYN_010_001 for SYN_FUN_010_001;
--创建函数
drop function if exists SYN_FUN_010_002(c bigint);
create or replace function SYN_FUN_010_002(c bigint) return int
as
b int := c;
begin
	for i in 1..c loop
		b:= b - 1;
	end loop;
	return b;
end;
/
--创建同义词
drop synonym if exists SYN_FUN_SYN_010_002;
create or replace synonym SYN_FUN_SYN_010_002 for SYN_FUN_010_002;
--创建函数
drop function if exists SYN_FUN_010_003(c bigint);
create or replace function SYN_FUN_010_003(c bigint) return int
as
b int := c;
begin
	for i in 1..c loop
		b:= b*1;
	end loop;
	return b;
end;
/
--创建同义词
drop synonym if exists SYN_FUN_SYN_010_003;
create or replace synonym SYN_FUN_SYN_010_003 for SYN_FUN_010_003;
--创建函数
drop function if exists SYN_FUN_010_004;
create or replace function SYN_FUN_010_004(c bigint)return int
as
b int := c;
begin
	for i in 1..c loop
		b:= b / 1;
	end loop;
	return b;
end;
/
--创建同义词
drop synonym if exists SYN_FUN_SYN_010_004;
create or replace synonym SYN_FUN_SYN_010_004 for SYN_FUN_010_004;
--查询
select avg(SYN_FUN_SYN_010_001(SYN_FUN_SYN_010_002(SYN_FUN_SYN_010_003(SYN_FUN_SYN_010_004(-1))))) from sys_dummy;
select SYN_FUN_SYN_010_001(avg(SYN_FUN_SYN_010_002(SYN_FUN_SYN_010_003(SYN_FUN_SYN_010_004(-1))))) from sys_dummy;
select SYN_FUN_SYN_010_001(SYN_FUN_SYN_010_002(avg(SYN_FUN_SYN_010_003(SYN_FUN_SYN_010_004(-1))))) from sys_dummy;
select SYN_FUN_SYN_010_001(SYN_FUN_SYN_010_002(SYN_FUN_SYN_010_003(avg(SYN_FUN_SYN_010_004(-1))))) from sys_dummy;
--清理环境
drop function if exists SYN_FUN_010_001(c int) cascade;
drop function if exists SYN_FUN_010_002(c bigint) cascade;
drop function if exists SYN_FUN_010_003(c bigint) cascade;
drop function if exists SYN_FUN_010_004(c bigint) cascade;
drop synonym if exists SYN_FUN_SYN_010_001;
drop synonym if exists SYN_FUN_SYN_010_002;
drop synonym if exists SYN_FUN_SYN_010_003;
drop synonym if exists SYN_FUN_SYN_010_004;