-- @testpoint: 在创建unique约束之后，向表中插入相同的数据，合理报错

drop table if exists t1;
create table t1(a int);
alter table t1 add constraint studentkey primary key(a);
alter table t1 add constraint unkey  unique (a);
insert into t1 values(1);
insert into t1 values(1);
drop table if exists t1;