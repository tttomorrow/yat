-- @testpoint: 修改类型长度小于已有数据长度时合理报错
drop table if exists t1 cascade;
create table t1(a varchar(5),c VARCHAR(10));
insert into t1 values('12345');
alter table t1 modify(a VARCHAR(3));
drop table if exists t1 cascade;