-- @testpoint:  多次统计分析表

drop table if exists t1;
create table t1(a int);
insert into t1 values(1);
insert into t1 values(2);
insert into t1 values(3);
insert into t1 values(4);
analyze  t1 ;
delete from t1;
insert into t1 values(5);
analyze  t1;
drop table if exists t1;
