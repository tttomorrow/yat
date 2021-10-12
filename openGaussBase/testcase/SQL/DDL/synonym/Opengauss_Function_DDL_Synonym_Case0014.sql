-- @testpoint: 自定义函数同义词作为入参与ACOS函数结合使用
--建自定义函数
drop function if exists SYN_FUN_014_001(c int) cascade;
create or replace function SYN_FUN_014_001(c int)return number
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
drop synonym if exists SYN_FUN_SYN_014_001;
create or replace synonym SYN_FUN_SYN_014_001 for SYN_FUN_014_001;
--创建函数
drop function if exists SYN_FUN_014_002(c bigint);
create or replace function SYN_FUN_014_002(c bigint) return int
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
drop synonym if exists SYN_FUN_SYN_014_002;
create or replace synonym SYN_FUN_SYN_014_002 for SYN_FUN_014_002;
--创建函数
drop function if exists SYN_FUN_014_003(c bigint);
create or replace function SYN_FUN_014_003(c bigint) return int
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
drop synonym if exists SYN_FUN_SYN_014_003;
create or replace synonym SYN_FUN_SYN_014_003 for SYN_FUN_014_003;
--创建函数
drop function if exists SYN_FUN_014_004;
create or replace function SYN_FUN_014_004(c bigint)return int
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
drop synonym if exists SYN_FUN_SYN_014_004;
create or replace synonym SYN_FUN_SYN_014_004 for SYN_FUN_014_004;
--查询
select ACOS(SYN_FUN_SYN_014_001(SYN_FUN_SYN_014_002(SYN_FUN_SYN_014_003(SYN_FUN_SYN_014_004(-1))))) from sys_dummy;
select SYN_FUN_SYN_014_001(ACOS(SYN_FUN_SYN_014_002(SYN_FUN_SYN_014_003(SYN_FUN_SYN_014_004(-1))))) from sys_dummy;
select SYN_FUN_SYN_014_001(SYN_FUN_SYN_014_002(ACOS(SYN_FUN_SYN_014_003(SYN_FUN_SYN_014_004(-1))))) from sys_dummy;
select SYN_FUN_SYN_014_001(SYN_FUN_SYN_014_002(SYN_FUN_SYN_014_003(ACOS(SYN_FUN_SYN_014_004(-1))))) from sys_dummy;
select ABS(SYN_FUN_SYN_014_001(ABS(SYN_FUN_SYN_014_002(ABS(SYN_FUN_SYN_014_003(ABS(SYN_FUN_SYN_014_004(-1))))))) )from sys_dummy;
--清理环境
drop function if exists SYN_FUN_014_001(c int) cascade;
drop function if exists SYN_FUN_014_002(c bigint) cascade;
drop function if exists SYN_FUN_014_003(c bigint) cascade;
drop function if exists SYN_FUN_014_004(c bigint) cascade;
drop synonym if exists SYN_FUN_SYN_014_001;
drop synonym if exists SYN_FUN_SYN_014_002;
drop synonym if exists SYN_FUN_SYN_014_003;
drop synonym if exists SYN_FUN_SYN_014_004;