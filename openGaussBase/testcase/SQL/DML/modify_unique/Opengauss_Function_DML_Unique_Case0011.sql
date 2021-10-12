-- @testpoint: 在存在主键的约束下创建unique约束

drop table if exists t1;
create table t1(a int);
alter table t1 add constraint studentkey primary key(a);
alter table t1 add constraint unkey  unique (a);
drop table if exists t1;