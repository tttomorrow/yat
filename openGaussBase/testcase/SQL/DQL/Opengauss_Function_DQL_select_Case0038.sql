-- @testpoint: DQL语法，结合内建函数转化字段

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


drop table if exists t_agg_join_004;
create table t_agg_join_004 (id int,c1 varchar(8000),c2 varchar(8000),c3 varchar(8000));
declare
begin
    for i in 1..2000 loop
        insert into t_agg_join_004 values (i,rpad('12',20,2),rpad('12',20,i),rpad('23',20,i));
    end loop;
    for i in 2001..4000 loop
        insert into t_agg_join_004 values (i,rpad('23',20,2),rpad('23',20,2),rpad('12',20,i));
    end loop;
    for i in 4001..8000 loop
        insert into t_agg_join_004 values (i,rpad('12',20,2),rpad('45',20,2),rpad('12',20,2));
    end loop;
end;
/

select trunc(sum(distinct power(b.c2,2)),-10), STDDEV(a.sal) from t_agg_join_003 a right join t_agg_join_004 b on a.id=b.id group by a.id order by 1,2;

drop table t_agg_join_003;
drop table t_agg_join_004;