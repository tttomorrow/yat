-- @testpoint: 创建表时，使用自定义函数的同义词设置检查约束
-- @modify at: 2020-11-25
--创建函数
drop function if exists SYN_FUN_001(a varchar) cascade;
create or replace function SYN_FUN_001 (a varchar) return int
as
b int;
begin
	b:=length(a);
	return b;
end;
/
--创建同义词
drop synonym if exists SYN_FUN_SYN_001;
create or replace  synonym  SYN_FUN_SYN_001 for SYN_FUN_001;
--建表
drop table if exists SYN_TAB_004;
create table SYN_TAB_004
(
	a int  check (a <SYN_FUN_SYN_001('uyfuigilhlgig')),
	b varchar(1024) check (SYN_FUN_SYN_001(b)<SYN_FUN_SYN_001('uyfuigilhlgig'))
);
--插入数据
insert into SYN_TAB_004 values(12,'a');
insert into SYN_TAB_004 values(1,'ahikhbojpg');
--查询
select * from SYN_TAB_004;
--清理环境
drop function if exists SYN_FUN_001(a varchar) cascade;
drop table if exists SYN_TAB_004 cascade;
drop synonym if exists SYN_FUN_SYN_001;