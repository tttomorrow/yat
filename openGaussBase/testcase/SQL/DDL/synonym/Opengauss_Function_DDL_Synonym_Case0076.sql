-- @testpoint: 使用truncate+同义词:合理报错
--建表
drop table if exists SYN_TAB_076 cascade;
create table SYN_TAB_076(a int,b clob);
insert into SYN_TAB_076 values(1,'a');
--建表的同义词
drop synonym if exists SYN_TAB_SYN_076_001 cascade;
create or replace synonym SYN_TAB_SYN_076_001 for SYN_TAB_076;
select * from SYN_TAB_SYN_076_001;
--清理同义词，报错
TRUNCATE SYN_TAB_SYN_076_001;
select * from SYN_TAB_SYN_076_001;
select * from SYN_TAB_SYN_076_001;
--清理环境
drop table if exists SYN_TAB_076_001 cascade;
drop table if exists SYN_TAB_076 cascade;
drop synonym if exists SYN_TAB_SYN_076_001 cascade;