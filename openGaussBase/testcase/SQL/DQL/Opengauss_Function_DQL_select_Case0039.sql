-- @testpoint: DQL语法，使用函数索引的字段

drop table if exists t_agg_join_001;
create table t_agg_join_001(id number,deptno number,name varchar2(20),sal number);
insert into t_agg_join_001 values(1,1,'1aa',120);
insert into t_agg_join_001 values(2,1,'2aa',300);
insert into t_agg_join_001 values(3,1,'3aa',100);
insert into t_agg_join_001 values(4,1,'4aa',99);
insert into t_agg_join_001 values(5,1,'5aa',90);
insert into t_agg_join_001 values(6,2,'6aa',87);
insert into t_agg_join_001 values(7,2,'7aa',500);
insert into t_agg_join_001 values(8,2,'8aa',200);
insert into t_agg_join_001 values(9,2,'9aa',20);
insert into t_agg_join_001 values(10,2,'10aa',30);
insert into t_agg_join_001 values(null,2,'10aa',30);
insert into t_agg_join_001 values(12,2,'10aa',null);


drop table if exists t_agg_join_003;
create table t_agg_join_003(id int,deptno int,name varchar(20),sal int,
id2 int,deptno2 int,name2 varchar(20),sal2 int,
id3 int,deptno3 int,name3 varchar(20),sal3 int,
id4 int,deptno4 int,name4 varchar(20),sal4 int);
insert into t_agg_join_003 values(1,1,'1aa',120,1,1,'1aa',120,1,1,'1aa',120,1,1,'1aa',120);
insert into t_agg_join_003 values(2,1,'2aa',300,2,1,'2aa',300,2,1,'2aa',300,2,1,'2aa',300);
insert into t_agg_join_003 values(3,1,'3aa',100,3,1,'3aa',100,3,1,'3aa',100,3,1,'3aa',100);
insert into t_agg_join_003 values(7,2,'7aa',500,7,2,'7aa',500,7,2,'7aa',500,7,2,'7aa',500);
insert into t_agg_join_003 values(8,2,'8aa',200,8,2,'8aa',200,8,2,'8aa',200,8,2,'8aa',200);
insert into t_agg_join_003 values(9,2,'9aa',20,9,2,'9aa',20,9,2,'9aa',20,9,2,'9aa',20);
insert into t_agg_join_003 values(null,2,'10aa',30,null,2,'10aa',30,null,2,'10aa',30,null,2,'10aa',30);


drop index if exists ind_t_agg_join_001;
create index index_003s on t_agg_join_003(upper(sal3));
select VAR_POP(a.sal3), max(abs(b.sal)) from t_agg_join_003 a full join t_agg_join_001 b on a.id2=b.id where a.sal3>=99 group by a.deptno order by 1,2;

select VAR_POP(b.deptno), max(abs(a.sal3)) from t_agg_join_003 a right join t_agg_join_001 b on a.id2=b.id where a.sal3>=99 group by a.deptno order by 1,2;

drop table t_agg_join_001;
drop table t_agg_join_003;

