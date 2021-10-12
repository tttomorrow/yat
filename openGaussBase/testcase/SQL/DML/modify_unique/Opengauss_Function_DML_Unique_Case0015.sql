-- @testpoint: 添加字段，先指定数据类型为blob，并且定义约束为unique,再次更新列属性为clob，约束为unique，合理报错

drop table if exists t1;
create table t1(a int);
alter table t1 add c blob unique;
alter table t1 add c clob unique;
drop table if exists t1;