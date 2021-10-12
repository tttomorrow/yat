-- @testpoint: 删除所有者为属主的同义词
-- @modify at: 2020-11-26
--建表
drop table if exists SYN_TAB_071_001 cascade;
create table SYN_TAB_071_001 (a int,b clob);
insert into SYN_TAB_071_001 values(1,'a');
--建表的同义词
drop synonym if exists SYN_TAB_SYN_071_001;
create or replace synonym SYN_TAB_SYN_071_001 for SYN_TAB_071_001;
select * from SYN_TAB_SYN_071_001;
--删除同义词
drop synonym SYN_TAB_SYN_071_001;
--查询同义词属主，不变
select usename from pg_user where usesysid=(select synowner from pg_synonym where synname='syn_tab_syn_071_001');
--清理环境
drop table if exists SYN_TAB_071_001 cascade;