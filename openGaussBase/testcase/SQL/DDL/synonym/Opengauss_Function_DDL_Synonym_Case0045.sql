-- @testpoint: 自定义函数同义词作为入参与length函数结合使用
-- @modify at: 2020-11-25
--创建函数
drop FUNCTION if exists SYN_FUN_002(a varchar);
create or replace function SYN_FUN_002 (a varchar) return varchar
as
b varchar(1024);
begin
	b:=a||a;
	return b;
end;
/
--创建同义词
drop synonym if exists SYN_FUN_SYN_002;
create or replace  synonym  SYN_FUN_SYN_002 for SYN_FUN_002;
--调用函数
select length(SYN_FUN_SYN_002('adcffa')) from sys_dummy;
select SYN_FUN_SYN_002(length(SYN_FUN_SYN_002('adcffa'))||SYN_FUN_SYN_002('adcffa')) from sys_dummy;
--清空环境
drop FUNCTION if exists SYN_FUN_002(a varchar) cascade;
drop synonym if exists SYN_FUN_SYN_002;