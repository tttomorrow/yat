-- @testpoint: 改变列的数据类型为blob和clob型，并添加unique约束，合理报错

drop table if exists t1;
create table t1(a int);
alter table t1 modify a blob unique;
alter table t1 modify a clob unique;
drop table if exists t1;
