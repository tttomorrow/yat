-- @testpoint: 自定义函数的同义词作为入参与SUBSTR函数结合使用
-- @modify at: 2020-11-25
--创建函数
drop FUNCTION if exists SYN_FUN_046(a varchar);
create or replace function SYN_FUN_046 (a varchar) return varchar
as
b varchar(1024);
begin
	b:=a||a;
	return b;
end;
/
--创建同义词
drop synonym if exists SYN_FUN_SYN_046;
create or replace synonym  SYN_FUN_SYN_046 for SYN_FUN_046;
--调用函数
select substr(SYN_FUN_SYN_046('adcffa'),10,2) from sys_dummy;
select SYN_FUN_SYN_046(substr(SYN_FUN_SYN_046('adcffa'),10,2)) from sys_dummy;
--清空环境
drop FUNCTION if exists SYN_FUN_046(a varchar) cascade;
drop synonym if exists SYN_FUN_SYN_046;