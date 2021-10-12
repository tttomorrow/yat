-- @testpoint: 创建表，数据类型为clob\
drop table if exists test12;
create table test12 (name clob);
insert into test12 (name) values('liuzi');
drop table if exists test12;