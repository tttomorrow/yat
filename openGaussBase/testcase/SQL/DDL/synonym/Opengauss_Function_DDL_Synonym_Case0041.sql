-- @testpoint: 创建表时，使用函数同义词设置默认值
-- @modify at: 2020-11-25
--创建函数
drop function if exists SYN_FUN_002(a varchar) cascade;
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
--建表并设置同义词默认值
drop table if exists SYN_TAB_004;
create table SYN_TAB_004
(
	a int  default SYN_FUN_SYN_002('uyfuigilhlgig'),
	b varchar(1024) default SYN_FUN_SYN_002('abcd')
);
--插入数据
insert into SYN_TAB_004(a) values(1);
--查询
select * from SYN_TAB_004 order by a;
--清空环境
drop table if exists SYN_TAB_004;
drop function if exists SYN_FUN_002(a varchar) cascade;
drop synonym if exists SYN_FUN_SYN_002;