-- @testpoint: 删除主键之后，再次更新unique约束

drop table if exists t1;
create table t1(a int);
alter table t1 add constraint studentkey primary key(a);
alter table t1 add constraint unkey  unique (a);
alter table t1 drop constraint studentkey;
alter table t1 add constraint unkey1  unique (a);
drop table if exists t1;