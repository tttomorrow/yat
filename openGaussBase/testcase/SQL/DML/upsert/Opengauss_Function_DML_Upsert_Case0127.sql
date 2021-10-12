-- @testpoint: upsert子查询select基础语法覆盖，不符合语法要求，合理报错

--创建upeset及子查询表，插入数据
drop table if exists t_dml_upsert_sub0127;
create table t_dml_upsert_sub0127 (a int,b int primary key,c text);
insert into t_dml_upsert_sub0127 values(generate_series(1,10),generate_series(1,10),'c-'||generate_series(1,10));
insert into t_dml_upsert_sub0127 values(generate_series(1,10),generate_series(11,20),'c-'||generate_series(1,10));
insert into t_dml_upsert_sub0127 values('',generate_series(21,30),'c-'||generate_series(1,10));
drop table if exists t_dml_upsert0127;
--创建upsert表，组合主键场景
create table t_dml_upsert0127 (a int , b text, c int not null, d text,primary key (a,b));
insert into t_dml_upsert0127 values (1,1,1),(2,2,2),(3,3,3),(4,4,4);
select * from t_dml_upsert0127;
analyze t_dml_upsert_sub0127;
analyze t_dml_upsert0127;

--distinct， muilt-set/single-set均支持
explain (costs off, verbose) select distinct(c),a from t_dml_upsert_sub0127 where a=4;
explain (costs off, verbose) insert into t_dml_upsert0127 values(1,1,3) on duplicate key update (d,c)= (select distinct(c),a from t_dml_upsert_sub0127 where a=4);
insert into t_dml_upsert0127 values(1,1,3) on duplicate key update (d,c)= (select distinct(c),a from t_dml_upsert_sub0127 where a=4);
select * from t_dml_upsert0127;
explain (costs off, verbose) select distinct(c) from t_dml_upsert_sub0127 where a=5;
explain (costs off, verbose) insert into t_dml_upsert0127 values(1,1,3) on duplicate key update d = (select distinct(c) from t_dml_upsert_sub0127 where a=5);
insert into t_dml_upsert0127 values(1,1,3) on duplicate key update d = (select distinct(c) from t_dml_upsert_sub0127 where a=5);
select * from t_dml_upsert0127;

--plain hint ，目前存在问题，待开发核实
--indexscan 方式的hint
explain (costs off, verbose) select /*+ indexscan(t_dml_upsert_sub0127)*/ c,a from t_dml_upsert_sub0127 where b>1 and a=1;
insert into t_dml_upsert0127 values(1,1,3) on duplicate key update (d,c)= ( select /*+ indexscan(t_dml_upsert_sub0127)*/ c,a from t_dml_upsert_sub0127 where b>1 and a=1);
explain (costs off, verbose) insert into t_dml_upsert0127 values(1,1,3) on duplicate key update (d,c)= ( select /*+ indexscan(t_dml_upsert_sub0127)*/ c,a from t_dml_upsert_sub0127 where b>1 and a=1);
select * from t_dml_upsert0127;
--tablescan 方式的hint
explain (costs off, verbose) select /*+ tablescan(t_dml_upsert_sub0127)*/ c,a from t_dml_upsert_sub0127 where b>1 and a=1;
insert into t_dml_upsert0127 values(1,1,3) on duplicate key update (d,c)= ( select /*+ tablescan(t_dml_upsert_sub0127)*/ c,a from t_dml_upsert_sub0127 where b>1 and a=1);
explain (costs off, verbose) insert into t_dml_upsert0127 values(1,1,3) on duplicate key update (d,c)= ( select /*+ tablescan(t_dml_upsert_sub0127)*/ c,a from t_dml_upsert_sub0127 where b>1 and a=1);
select * from t_dml_upsert0127;

--limit,muilt-set不支持，报错；single-set支持
insert into t_dml_upsert0127 values(1,1,3) on duplicate key update (c,d) = (select c,b from t_dml_upsert_sub0127 where a>4 limit 1);
explain (costs off, verbose) select c from t_dml_upsert_sub0127 where a>4 limit 1;
insert into t_dml_upsert0127 values(1,1,3) on duplicate key update d = (select c from t_dml_upsert_sub0127 where a>4 limit 1);
select * from t_dml_upsert0127;
explain (costs off, verbose) insert into t_dml_upsert0127 values(1,1,3) on duplicate key update d = (select c from t_dml_upsert_sub0127 where a>4 limit 1);

--limit offset，muilt-set不支持，报错；single-set支持
insert into t_dml_upsert0127 values(1,1,3) on duplicate key update (c,d)= (select c,b from t_dml_upsert_sub0127 where a>4 limit 1 offset 5);
explain (costs off, verbose) select c from t_dml_upsert_sub0127 where a>4 limit 1 offset 5;
insert into t_dml_upsert0127 values(1,1,3) on duplicate key update d = (select c from t_dml_upsert_sub0127 where a>4 limit 1 offset 5);
select * from t_dml_upsert0127;
explain (costs off, verbose) insert into t_dml_upsert0127 values(1,1,3) on duplicate key update d = (select c from t_dml_upsert_sub0127 where a>4 limit 1 offset 5);

--offset，muilt-set不支持，报错；single-set支持
insert into t_dml_upsert0127 values(1,1,3) on duplicate key update (c,d)= (select c,b from t_dml_upsert_sub0127 where a>4 offset 5);
explain (costs off, verbose) select b from t_dml_upsert_sub0127 where b>4 and a =10 order by b asc offset 1;
insert into t_dml_upsert0127 values(1,1,3) on duplicate key update d = (select b from t_dml_upsert_sub0127 where b>4 and a =10 order by b asc offset 1);
explain (costs off, verbose) insert into t_dml_upsert0127 values(1,1,3) on duplicate key update d = (select b from t_dml_upsert_sub0127 where b>4 and a =10 order by b asc offset 1);
select * from t_dml_upsert0127;

--FETCH，muilt-set不支持，报错；single-set支持
insert into t_dml_upsert0127 values(1,1,3) on duplicate key update (c,d)= (select c,b from t_dml_upsert_sub0127 where b>4 offset 2 fetch next 1 row only);
explain (costs off, verbose) select b from t_dml_upsert_sub0127 where b>4 offset 2 fetch next 1 row only;
insert into t_dml_upsert0127 values(1,1,3) on duplicate key update d= (select b from t_dml_upsert_sub0127 where b>4 offset 2 fetch next 1 row only);
select * from t_dml_upsert0127;
explain (costs off, verbose) insert into t_dml_upsert0127 values(1,1,3) on duplicate key update d= (select b from t_dml_upsert_sub0127 where b>4 offset 2 fetch next 1 row only);

--order by ，muilt-set不支持，报错；single-set支持
insert into t_dml_upsert0127 values(2,2,3) on duplicate key update (c,d) = (select c,b from t_dml_upsert_sub0127 where b=4 order by b ASC);
explain (costs off, verbose) select a from t_dml_upsert_sub0127 where b=4 order by b ASC;
insert into t_dml_upsert0127 values(2,2,3) on duplicate key update c= (select a from t_dml_upsert_sub0127 where b=4 order by b ASC);
select * from t_dml_upsert0127;
explain (costs off, verbose) insert into t_dml_upsert0127 values(2,2,3) on duplicate key update d= (select c from t_dml_upsert_sub0127 where b=4 order by b ASC);

--CTE with子句，muilt-set不支持，报错；single-set支持
insert into t_dml_upsert0127 values(3,3,4) on duplicate key update (c,d)= (with temp_tb(i,j,k) as(select a,c,b from t_dml_upsert_sub0127) select i,j from temp_tb where k = '7');
explain (costs off, verbose) with temp_tb(i,j,k) as(select a,c,b from t_dml_upsert_sub0127) select i from temp_tb where k = '7';
insert into t_dml_upsert0127 values(3,3,4) on duplicate key update c = (with temp_tb(i,j,k) as(select a,c,b from t_dml_upsert_sub0127) select i from temp_tb where k = '7');
select * from t_dml_upsert0127;
explain (costs off, verbose) insert into t_dml_upsert0127 values(3,3,4) on duplicate key update c = (with temp_tb(i,j,k) as(select a,c,b from t_dml_upsert_sub0127) select i from temp_tb where k = '7');

--order by nulls ;muilt-set不支持，报错；single-set支持
insert into t_dml_upsert0127 values(2,2,3) on duplicate key update (c,d) =(select a, avg(b) from t_dml_upsert_sub0127 group by a having avg(b)>10 order by a nulls last);
explain (costs off, verbose) select avg(b) from t_dml_upsert_sub0127 group by a having avg(b)>13 order by a nulls last limit 1;
insert into t_dml_upsert0127 values(2,2,3) on duplicate key update d =(select avg(b) from t_dml_upsert_sub0127 group by a having avg(b)>13 order by a nulls last limit 1);
explain (costs off, verbose) insert into t_dml_upsert0127 values(2,2,3) on duplicate key update d =(select avg(b) from t_dml_upsert_sub0127 group by a having avg(b)>13 order by a nulls last limit 1);
select * from t_dml_upsert0127;
explain (costs off, verbose) select avg(b) from t_dml_upsert_sub0127 group by a having avg(b)>13 order by a nulls first limit 1;
insert into t_dml_upsert0127 values(2,2,3) on duplicate key update d =(select avg(b) from t_dml_upsert_sub0127 group by a having avg(b)>13 order by a nulls first limit 1);
select * from t_dml_upsert0127;
explain (costs off, verbose) insert into t_dml_upsert0127 values(2,2,3) on duplicate key update d =(select avg(b) from t_dml_upsert_sub0127 group by a having avg(b)>13 order by a nulls first limit 1);

--group by having; muilt-set/single-set均支持
explain (costs off, verbose) select a,avg(b) from t_dml_upsert_sub0127 group by a having avg(b)=15;
insert into t_dml_upsert0127 values(2,2,3) on duplicate key update (c,d) = (select a,avg(b) from t_dml_upsert_sub0127 group by a having avg(b)=15);
select * from t_dml_upsert0127;
explain (costs off, verbose) insert into t_dml_upsert0127 values(2,2,3) on duplicate key update (c,d) = (select a,avg(b) from t_dml_upsert_sub0127 group by a having avg(b)=15);
explain (costs off, verbose) select avg(b) from t_dml_upsert_sub0127 group by a having avg(b)>10 order by a asc limit 1;
insert into t_dml_upsert0127 values(2,2,3) on duplicate key update d = (select avg(b) from t_dml_upsert_sub0127 group by a having avg(b)>10 order by a asc limit 1);
select * from t_dml_upsert0127;
explain (costs off, verbose) insert into t_dml_upsert0127 values(2,2,3) on duplicate key update d = (select avg(b) from t_dml_upsert_sub0127 group by a having avg(b)>10 order by a asc limit 1);

--group by cube; muilt-set/single-set均支持
explain (costs off, verbose) select a,avg(b) from t_dml_upsert_sub0127 group by CUBE(a) having avg(b)= 10;
insert into t_dml_upsert0127 values(2,2,3) on duplicate key update (c,d) = (select a,avg(b) from t_dml_upsert_sub0127 group by CUBE(a) having avg(b)= 10);
select * from t_dml_upsert0127;
explain (costs off, verbose) insert into t_dml_upsert0127 values(2,2,3) on duplicate key update (c,d) = (select a,avg(b) from t_dml_upsert_sub0127 group by CUBE(a) having avg(b)= 10);
explain (costs off, verbose) select a from t_dml_upsert_sub0127 group by CUBE(a) having avg(b)= 11;
insert into t_dml_upsert0127 values(2,2,3) on duplicate key update d = (select a from t_dml_upsert_sub0127 group by CUBE(a) having avg(b)= 11);
select * from t_dml_upsert0127;
explain (costs off, verbose) insert into t_dml_upsert0127 values(2,2,3) on duplicate key update d = (select a from t_dml_upsert_sub0127 group by CUBE(a) having avg(b)= 11);

--window ;muilt-set不支持/single-set支持
insert into t_dml_upsert0127 values(2,2,3) on duplicate key update (c,d) = (select b,count(c) over window1 typecount from t_dml_upsert_sub0127 where b =11 window window1 as (partition by a));
explain (costs off, verbose) select count(c) over window1 typecount from t_dml_upsert_sub0127 where b =11 window window1 as (partition by a);
insert into t_dml_upsert0127 values(2,2,3) on duplicate key update c = (select count(c) over window1 typecount from t_dml_upsert_sub0127 where b =11 window window1 as (partition by a));
select * from t_dml_upsert0127;
explain (costs off, verbose) insert into t_dml_upsert0127 values(2,2,3) on duplicate key update c = (select count(c) over window1 typecount from t_dml_upsert_sub0127 where b =11 window window1 as (partition by a));

--union ;muilt-set不支持/single-set支持
insert into t_dml_upsert0127 values(2,2,3) on duplicate key update (c,d) = (select a,b from t_dml_upsert_sub0127 where a =1 union select a,b from t_dml_upsert_sub0127 where a = 2);
explain (costs off, verbose) select b from t_dml_upsert_sub0127 where a =1 union select b from t_dml_upsert_sub0127 where a = 2 order by b desc limit 1;
insert into t_dml_upsert0127 values(2,2,3) on duplicate key update d = (select b from t_dml_upsert_sub0127 where a =1 union select b from t_dml_upsert_sub0127 where a = 2 order by b desc limit 1);
select * from t_dml_upsert0127;
explain (costs off, verbose) insert into t_dml_upsert0127 values(2,2,3) on duplicate key update d = (select b from t_dml_upsert_sub0127 where a =1 union select b from t_dml_upsert_sub0127 where a = 2 order by b desc limit 1);

--except ;muilt-set不支持/single-set支持
insert into t_dml_upsert0127 values(2,2,3) on duplicate key update (c,d) = (select a,c from t_dml_upsert_sub0127 where b>3 except select a,c from t_dml_upsert_sub0127 where b>4);
explain (costs off, verbose) select c from t_dml_upsert_sub0127 where b>3 except select c from t_dml_upsert_sub0127 where a = 4 order by c desc limit 1;
insert into t_dml_upsert0127 values(2,2,3) on duplicate key update d = (select c from t_dml_upsert_sub0127 where b>3 except select c from t_dml_upsert_sub0127 where a = 4 order by c desc limit 1);
select * from t_dml_upsert0127;
explain (costs off, verbose) insert into t_dml_upsert0127 values(2,2,3) on duplicate key update d = (select c from t_dml_upsert_sub0127 where b>3 except select c from t_dml_upsert_sub0127 where a = 4 order by c desc limit 1);

--intersect ;muilt-set不支持/single-set支持
insert into t_dml_upsert0127 values(2,2,3) on duplicate key update (c,d) = (select a,c from t_dml_upsert_sub0127 where b>3 intersect select a,c from t_dml_upsert_sub0127 where b>4);
explain (costs off, verbose) select c from t_dml_upsert_sub0127 where b>3 intersect select c from t_dml_upsert_sub0127 where a < 4 order by c desc limit 1;
insert into t_dml_upsert0127 values(2,2,3) on duplicate key update d = (select c from t_dml_upsert_sub0127 where b>3 intersect select c from t_dml_upsert_sub0127 where a < 4 order by c desc limit 1);
select * from t_dml_upsert0127;
explain (costs off, verbose) insert into t_dml_upsert0127 values(2,2,3) on duplicate key update d = (select c from t_dml_upsert_sub0127 where b>3 intersect select c from t_dml_upsert_sub0127 where a < 4 order by c desc limit 1);

--order by NLS_SORT ;single-set支持
insert into t_dml_upsert_sub0127 values(generate_series(1,10),generate_series(31,40),'C-'||generate_series(1,10));
explain (costs off, verbose) select b from t_dml_upsert_sub0127 order by NLSSORT( c, 'NLS_SORT = generic_m_ci') limit 1;
insert into t_dml_upsert0127 values(2,2,3) on duplicate key update d= (select b from t_dml_upsert_sub0127 order by NLSSORT( c, 'NLS_SORT = generic_m_ci') limit 1);
explain (costs off, verbose) insert into t_dml_upsert0127 values(2,2,3) on duplicate key update d= (select b from t_dml_upsert_sub0127 order by NLSSORT( c, 'NLS_SORT = generic_m_ci') limit 1);
select * from t_dml_upsert0127;
explain (costs off, verbose) select b from t_dml_upsert_sub0127 order by c limit 1;
insert into t_dml_upsert0127 values(2,2,3) on duplicate key update d= (select b from t_dml_upsert_sub0127 order by c limit 1);
explain (costs off, verbose) insert into t_dml_upsert0127 values(2,2,3) on duplicate key update d= (select b from t_dml_upsert_sub0127 order by c limit 1);
select * from t_dml_upsert0127;

--for update ;muilt-set不支持/single-set支持
insert into t_dml_upsert0127 values(2) on duplicate key update (b,c) = (select b,c from t_dml_upsert_sub0127 where a = excluded.a for update);
insert into t_dml_upsert0127 values(2) on duplicate key update b= (select b from t_dml_upsert_sub0127 where a = excluded.a for update);
select * from t_dml_upsert0127;

--数据处理
drop table if exists t_dml_upsert0127;
drop table if exists t_dml_upsert_sub0127;