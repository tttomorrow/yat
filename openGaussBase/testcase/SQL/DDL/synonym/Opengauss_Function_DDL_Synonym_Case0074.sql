-- @testpoint: 删除同义词+CASCADE选项：成功
-- @modify at: 2020-11-26
--建表
drop table if exists SYN_TAB_074_001 cascade;
create table SYN_TAB_074_001 (a int,b clob);
--插入数据
insert into SYN_TAB_074_001 values(1,'a');
--建表的同义词
drop synonym if exists SYN_TAB_SYN_074_001;
create or replace synonym SYN_TAB_SYN_074_001 for SYN_TAB_074_001;
select * from SYN_TAB_SYN_074_001;
--删除同义词
drop synonym  SYN_TAB_SYN_074_001 cascade;
--删表
drop table if exists SYN_TAB_074_001 cascade;