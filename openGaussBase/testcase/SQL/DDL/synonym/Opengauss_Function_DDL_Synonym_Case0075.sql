-- @testpoint: 删除同义词+RESTRICT选项,有依赖对象，合理报错
-- @modify at: 2020-11-26
--建表
drop table if exists SYN_TAB_075_001 cascade;
create table SYN_TAB_075_001 (a int,b clob);
--插入数据
insert into SYN_TAB_075_001 values(1,'a');
--建表的同义词
drop synonym if exists SYN_TAB_SYN_075_001 cascade;
create or replace synonym SYN_TAB_SYN_075_001 for SYN_TAB_075_001;
select * from SYN_TAB_SYN_075_001;
--建视图同义词
drop view if exists v1;
create view v1 as select * from SYN_TAB_SYN_075_001;
--删除同义词，报错
drop synonym  SYN_TAB_SYN_075_001 ;
drop synonym  SYN_TAB_SYN_075_001 RESTRICT;
--清理数据
drop synonym if exists SYN_TAB_SYN_075_001 cascade;
drop table if exists SYN_TAB_075_001 cascade;