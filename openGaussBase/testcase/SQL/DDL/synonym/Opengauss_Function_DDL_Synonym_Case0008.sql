-- @testpoint: 自定义函数同义词作为入参与其他自定义函数同义词嵌套使用
-- @modify at: 2020-11-25
--创建函数
drop function if exists SYN_FUN_008_001(c bigint);
create or replace function SYN_FUN_008_001(c bigint) return int
as
b int := c;
begin
	for i in 1..c loop
		b:= b - 1;
	end loop;
	return b;
end;
/
drop synonym if exists SYN_FUN_SYN_008_001;
--创建同义词
create or replace synonym SYN_FUN_SYN_008_001 for SYN_FUN_008_001;
--创建函数
drop function if exists SYN_FUN_008_002(c bigint);
create or replace function SYN_FUN_008_002(c bigint) return int
as
b int := c;
begin
	for i in 1..c loop
		b:= b - 1;
	end loop;
	return b;
end;
/
drop synonym if exists SYN_FUN_SYN_008_002;
--创建同义词
create or replace synonym SYN_FUN_SYN_008_002 for SYN_FUN_008_002;
--创建函数
drop function if exists SYN_FUN_008_003(c bigint);
create or replace function SYN_FUN_008_003(c bigint) return int
as
b int := c;
begin
	for i in 1..c loop
		b:= b*1;
	end loop;
	return b;
end;
/
drop synonym if exists SYN_FUN_SYN_008_003;
--创建同义词
create or replace synonym SYN_FUN_SYN_008_003 for SYN_FUN_008_003;
--创建函数
drop function if exists SYN_FUN_008_004;
create or replace function SYN_FUN_008_004(c bigint)return int
as
b int := c;
begin
	for i in 1..c loop
		b:= b / 1;
	end loop;
	return b;
end;
/
drop synonym if exists SYN_FUN_SYN_008_004;
--创建同义词
create or replace synonym SYN_FUN_SYN_008_004 for SYN_FUN_008_004;
--嵌套调用
select SYN_FUN_SYN_008_004(-1) from sys_dummy;
select SYN_FUN_SYN_008_003(SYN_FUN_SYN_008_004(-1)) from sys_dummy;
select SYN_FUN_SYN_008_002(SYN_FUN_SYN_008_003(SYN_FUN_SYN_008_004(-1))) from sys_dummy;
select SYN_FUN_SYN_008_001(SYN_FUN_SYN_008_002(SYN_FUN_SYN_008_003(SYN_FUN_SYN_008_004(-1)))) from sys_dummy;
--清理环境
drop function if exists SYN_FUN_008_001(c bigint) cascade;
drop function if exists SYN_FUN_008_002(c bigint) cascade;
drop function if exists SYN_FUN_008_003(c bigint) cascade;
drop function if exists SYN_FUN_008_004(c bigint) cascade;
drop synonym SYN_FUN_SYN_008_001;
drop synonym SYN_FUN_SYN_008_002;
drop synonym SYN_FUN_SYN_008_003;
drop synonym SYN_FUN_SYN_008_004;