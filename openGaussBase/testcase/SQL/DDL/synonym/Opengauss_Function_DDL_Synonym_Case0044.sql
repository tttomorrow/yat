-- @testpoint: 创建表后，修改表的检查约束中使用自定义函数的同义词，违反检查约束，合理报错
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
--分别删除、增加表的约束
alter table SYN_TAB_004 drop CONSTRAINT "syn_tab_004_a_check";
alter table SYN_TAB_004 add constraint syn_tab_004_a_check check (a <SYN_FUN_SYN_001('uyfui'));
alter table SYN_TAB_004 drop CONSTRAINT "syn_tab_004_b_check";
alter table SYN_TAB_004 add constraint syn_tab_004_b_check check (SYN_FUN_SYN_001(b)<SYN_FUN_SYN_001('uyfui'));
--插入数据,报错
insert into SYN_TAB_004 values(14,'a');
insert into SYN_TAB_004 values(1,'ahikhbojpgfghpjho9ggio');
--查询
select * from SYN_TAB_004;
--清理环境
drop function if exists SYN_FUN_001(a varchar) cascade;
drop table if exists SYN_TAB_004 cascade;
drop synonym if exists SYN_FUN_SYN_001;
