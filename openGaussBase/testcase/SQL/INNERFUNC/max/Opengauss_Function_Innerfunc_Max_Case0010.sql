-- @testpoint: max函数使用在表达式和索引中
DROP TABLE if exists t1;
create table t1(a int,  b int);
create index idx_t1_1 on t1(a);
insert into t1 values(1,1);
insert into t1 values(2,1);
insert into t1 values(3,1);
insert into t1 values(4,1);
select max(a) +1 from t1 where a >=1;
DROP TABLE if exists t1;