-- @testpoint: 在表中插入相同的数据，然后修改约束为unique，合理报错

drop table if exists t1;
create table t1(a int);
insert into t1 values(1);
insert into t1 values(1);
alter table t1  add constraint ua unique (a);
drop table if exists t1;

