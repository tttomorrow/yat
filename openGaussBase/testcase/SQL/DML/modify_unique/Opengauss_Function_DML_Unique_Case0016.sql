-- @testpoint: 添加字段，指定数据类型为非blob,clob 类型，并且定义约束为unique，执行成功

drop table if exists t1;
create table t1(a int);
alter table t1 add c blob unique;
alter table t1 add d char(10) unique;
drop table if exists t1;