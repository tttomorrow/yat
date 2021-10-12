-- @testpoint: 在有unique约束的前提下，创建主键约束

drop table if exists t1;
create table t1(a int);
insert into t1 values(1);
insert into t1 values(11);
alter table t1  add constraint ua unique (a);
alter table t1 add constraint studentkey primary key(a);
drop table if exists t1;
