-- @testpoint: 自定义函数同义词作为入参与ABS函数结合使用
-- @modify at: 2020-11-25
--建自定义函数
drop function if exists SYN_FUN_001(c bigint) cascade;
create or replace function SYN_FUN_001(c int)return number
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
drop synonym if exists SYN_FUN_SYN_001;
create or replace synonym SYN_FUN_SYN_001 for SYN_FUN_001;
--创建函数
drop function if exists SYN_FUN_002(c bigint);
create or replace function SYN_FUN_002(c bigint) return int
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
drop synonym if exists SYN_FUN_SYN_002;
create or replace synonym SYN_FUN_SYN_002 for SYN_FUN_002;
--创建函数
drop function if exists SYN_FUN_003(c bigint);
create or replace function SYN_FUN_003(c bigint) return int
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
drop synonym if exists SYN_FUN_SYN_003;
create or replace synonym SYN_FUN_SYN_003 for SYN_FUN_003;
--创建函数
drop function if exists SYN_FUN_004;
create or replace function SYN_FUN_004(c bigint)return int
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
drop synonym if exists SYN_FUN_SYN_004;
create or replace synonym SYN_FUN_SYN_004 for SYN_FUN_004;
--查询
select ABS(SYN_FUN_SYN_001(SYN_FUN_SYN_002(SYN_FUN_SYN_003(SYN_FUN_SYN_004(-1)))) )from sys_dummy;
select SYN_FUN_SYN_001(ABS(SYN_FUN_SYN_002(SYN_FUN_SYN_003(SYN_FUN_SYN_004(-1))))) from sys_dummy;
select SYN_FUN_SYN_001(SYN_FUN_SYN_002(ABS(SYN_FUN_SYN_003(SYN_FUN_SYN_004(-1))))) from sys_dummy;
select SYN_FUN_SYN_001(SYN_FUN_SYN_002(SYN_FUN_SYN_003(ABS(SYN_FUN_SYN_004(-1))))) from sys_dummy;
select ABS(SYN_FUN_SYN_001(ABS(SYN_FUN_SYN_002(ABS(SYN_FUN_SYN_003(ABS(SYN_FUN_SYN_004(-1))))))) )from sys_dummy;
--清理环境
drop function if exists SYN_FUN_001(c bigint) cascade;
drop function if exists SYN_FUN_002(c bigint) cascade;
drop function if exists SYN_FUN_003(c bigint) cascade;
drop function if exists SYN_FUN_004(c bigint) cascade;
drop synonym if exists SYN_FUN_SYN_001;
drop synonym if exists SYN_FUN_SYN_002;
drop synonym if exists SYN_FUN_SYN_003;
drop synonym if exists SYN_FUN_SYN_004;