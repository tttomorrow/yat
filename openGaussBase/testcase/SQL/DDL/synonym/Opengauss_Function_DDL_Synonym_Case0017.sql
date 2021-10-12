-- @testpoint: 自定义函数同义词作为入参与EXP函数结合使用
--建自定义函数
drop function if exists SYN_FUN_017_001(c int) cascade;
create or replace function SYN_FUN_017_001(c int)return number
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
drop synonym if exists SYN_FUN_SYN_017_001;
create or replace synonym SYN_FUN_SYN_017_001 for SYN_FUN_017_001;
--创建函数
drop function if exists SYN_FUN_017_002(c bigint);
create or replace function SYN_FUN_017_002(c bigint) return int
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
drop synonym if exists SYN_FUN_SYN_017_002;
create or replace synonym SYN_FUN_SYN_017_002 for SYN_FUN_017_002;
--创建函数
drop function if exists SYN_FUN_017_003(c bigint);
create or replace function SYN_FUN_017_003(c bigint) return int
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
drop synonym if exists SYN_FUN_SYN_017_003;
create or replace synonym SYN_FUN_SYN_017_003 for SYN_FUN_017_003;
--创建函数
drop function if exists SYN_FUN_017_004;
create or replace function SYN_FUN_017_004(c bigint)return int
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
drop synonym if exists SYN_FUN_SYN_017_004;
create or replace synonym SYN_FUN_SYN_017_004 for SYN_FUN_017_004;
--查询
select EXP(SYN_FUN_SYN_017_001(SYN_FUN_SYN_017_002(SYN_FUN_SYN_017_003(SYN_FUN_SYN_017_004(-1)))) )from sys_dummy;
select SYN_FUN_SYN_017_001(EXP(SYN_FUN_SYN_017_002(SYN_FUN_SYN_017_003(SYN_FUN_SYN_017_004(-1))))) from sys_dummy;
select SYN_FUN_SYN_017_001(SYN_FUN_SYN_017_002(EXP(SYN_FUN_SYN_017_003(SYN_FUN_SYN_017_004(-1))))) from sys_dummy;
select SYN_FUN_SYN_017_001(SYN_FUN_SYN_017_002(SYN_FUN_SYN_017_003(EXP(SYN_FUN_SYN_017_004(-1))))) from sys_dummy;
select EXP(SYN_FUN_SYN_017_001(EXP(SYN_FUN_SYN_017_002(EXP(SYN_FUN_SYN_017_003(EXP(SYN_FUN_SYN_017_004(-1))))))) )from sys_dummy;
--清理环境
drop function if exists SYN_FUN_017_001(c int) cascade;
drop function if exists SYN_FUN_017_002(c bigint) cascade;
drop function if exists SYN_FUN_017_003(c bigint) cascade;
drop function if exists SYN_FUN_017_004(c bigint) cascade;
drop synonym if exists SYN_FUN_SYN_017_001;
drop synonym if exists SYN_FUN_SYN_017_002;
drop synonym if exists SYN_FUN_SYN_017_003;
drop synonym if exists SYN_FUN_SYN_017_004;