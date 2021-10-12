-- @testpoint: 修改约束之后，添加not null 约束执行成功

drop table if exists t1;
create table t1(a int);
insert into t1 values(1);
insert into t1 values(11);
alter table t1  add constraint ua unique (a);
alter table t1 modify a not null;
drop table if exists t1;