-- @testpoint: 添加字段，不指定数据类型，定义约束为unique，合理报错

drop table if exists t1;
create table t1(a int);
alter table t1 add constraint studentkey primary key(a);
alter table t1 add c unique;
drop table if exists t1;


