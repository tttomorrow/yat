-- @testpoint: 结合case when条件查询，部分测试点合理报错

drop table if exists t2;
create table t2 (a int,b char(10));
insert into t2 values(10,'abc');
insert into t2 values(20,'abc');
insert into t2 values(20,'abc');
insert into t2 values(82,'cd');
insert into t2 values(43,'cd');
insert into t2 values(89,'abc');
select case when user='SYS' then 'a' else 'b' end from t2;
drop table if exists t2;