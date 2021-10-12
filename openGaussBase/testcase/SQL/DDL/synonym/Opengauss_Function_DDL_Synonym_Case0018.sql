-- @testpoint: 自定义函数同义词作为入参与FLOOR函数结合使用
--建自定义函数
drop function if exists SYN_FUN_018_001(c int) cascade;
create or replace function SYN_FUN_018_001(c int)return number
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
drop synonym if exists SYN_FUN_SYN_018_001;
create or replace synonym SYN_FUN_SYN_018_001 for SYN_FUN_018_001;
--创建函数
drop function if exists SYN_FUN_018_002(c bigint);
create or replace function SYN_FUN_018_002(c bigint) return int
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
drop synonym if exists SYN_FUN_SYN_018_002;
create or replace synonym SYN_FUN_SYN_018_002 for SYN_FUN_018_002;
--创建函数
drop function if exists SYN_FUN_018_003(c bigint);
create or replace function SYN_FUN_018_003(c bigint) return int
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
drop synonym if exists SYN_FUN_SYN_018_003;
create or replace synonym SYN_FUN_SYN_018_003 for SYN_FUN_018_003;
--创建函数
drop function if exists SYN_FUN_018_004;
create or replace function SYN_FUN_018_004(c bigint)return int
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
drop synonym if exists SYN_FUN_SYN_018_004;
create or replace synonym SYN_FUN_SYN_018_004 for SYN_FUN_018_004;
--查询
select FLOOR(SYN_FUN_SYN_018_001(SYN_FUN_SYN_018_002(SYN_FUN_SYN_018_003(SYN_FUN_SYN_018_004(-1)))) )from sys_dummy;
select SYN_FUN_SYN_018_001(FLOOR(SYN_FUN_SYN_018_002(SYN_FUN_SYN_018_003(SYN_FUN_SYN_018_004(-1))))) from sys_dummy;
select SYN_FUN_SYN_018_001(SYN_FUN_SYN_018_002(FLOOR(SYN_FUN_SYN_018_003(SYN_FUN_SYN_018_004(-1))))) from sys_dummy;
select SYN_FUN_SYN_018_001(SYN_FUN_SYN_018_002(SYN_FUN_SYN_018_003(FLOOR(SYN_FUN_SYN_018_004(-1))))) from sys_dummy;
select FLOOR(SYN_FUN_SYN_018_001(FLOOR(SYN_FUN_SYN_018_002(FLOOR(SYN_FUN_SYN_018_003(FLOOR(SYN_FUN_SYN_018_004(-1))))))) )from sys_dummy;
--清理环境
drop function if exists SYN_FUN_018_001(c int) cascade;
drop function if exists SYN_FUN_018_002(c bigint) cascade;
drop function if exists SYN_FUN_018_003(c bigint) cascade;
drop function if exists SYN_FUN_018_004(c bigint) cascade;
drop synonym if exists SYN_FUN_SYN_018_001;
drop synonym if exists SYN_FUN_SYN_018_002;
drop synonym if exists SYN_FUN_SYN_018_003;
drop synonym if exists SYN_FUN_SYN_018_004;
