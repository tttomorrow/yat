-- @testpoint: upsert子查询多表关联查询覆盖，不符合语法要求，合理报错

--创建upeset及子查询表，插入数据
drop table if exists t_dml_upsert_sub0129_01;
create table t_dml_upsert_sub0129_01 (b int,c text);
insert into t_dml_upsert_sub0129_01 values(generate_series(1,10),'c-'||generate_series(1,10));
insert into t_dml_upsert_sub0129_01 values(generate_series(11,20),'c-'||generate_series(11,20));
drop table if exists t_dml_upsert_sub0129_02;
create table t_dml_upsert_sub0129_02 (b int,d text);
insert into t_dml_upsert_sub0129_02 values(generate_series(1,10),'d-'||generate_series(1,10));
--创建upsert表，组合主键场景
drop table if exists t_dml_upsert0129;
create table t_dml_upsert0129 (a int primary key , b text, c text, d text);
insert into t_dml_upsert0129 values (1,1,1),(2,2,2),(3,3,3),(4,4,4);
analyze t_dml_upsert_sub0129_01;
analyze t_dml_upsert_sub0129_02;
analyze t_dml_upsert0129;

select * from t_dml_upsert0129;
--join; muilt-set/single-set均支持
explain (costs off, verbose) select tb1.c,tb2.d from t_dml_upsert_sub0129_01 tb1 join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb1.b = 2;
insert into t_dml_upsert0129 values(2,2,3) on duplicate key update(c,d)=(select tb1.c,tb2.d from t_dml_upsert_sub0129_01 tb1 join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb1.b = 2);
select * from t_dml_upsert0129;
explain (costs off, verbose) insert into t_dml_upsert0129 values(2,2,3) on duplicate key update(c,d)=(select tb1.c,tb2.d from t_dml_upsert_sub0129_01 tb1 join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb1.b = 2);
explain (costs off, verbose) select tb1.c from t_dml_upsert_sub0129_01 tb1 join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb2.d = 'd-10';
insert into t_dml_upsert0129 values(2,2,3) on duplicate key update c =(select tb1.c from t_dml_upsert_sub0129_01 tb1 join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb2.d = 'd-10');
select * from t_dml_upsert0129;
explain (costs off, verbose) insert into t_dml_upsert0129 values(2,2,3) on duplicate key update c =(select tb1.c from t_dml_upsert_sub0129_01 tb1 join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb2.d = 'd-10');

--right join; muilt-set/single-set均支持
explain (costs off, verbose) select tb1.c,tb2.d from t_dml_upsert_sub0129_01 tb1 right join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb1.b = 3;
insert into t_dml_upsert0129 values(3,2,3) on duplicate key update(c,d)=(select tb1.c,tb2.d from t_dml_upsert_sub0129_01 tb1 right join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb1.b = 3);
select * from t_dml_upsert0129;
explain (costs off, verbose) insert into t_dml_upsert0129 values(2,2,3) on duplicate key update(c,d)=(select tb1.c,tb2.d from t_dml_upsert_sub0129_01 tb1 right join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb1.b = 3);
explain (costs off, verbose) select tb1.c from t_dml_upsert_sub0129_01 tb1 right join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb2.d = 'd-10';
insert into t_dml_upsert0129 values(3,2,3) on duplicate key update c =(select tb1.c from t_dml_upsert_sub0129_01 tb1 right join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb2.d = 'd-10');
select * from t_dml_upsert0129;
explain (costs off, verbose) insert into t_dml_upsert0129 values(2,2,3) on duplicate key update c =(select tb1.c from t_dml_upsert_sub0129_01 tb1 right join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb2.d = 'd-10');

--left join; muilt-set/single-set均支持
explain (costs off, verbose) select tb1.c,tb2.d from t_dml_upsert_sub0129_01 tb1 left join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb1.b = 13;
insert into t_dml_upsert0129 values(3,2,3) on duplicate key update(c,d)=(select tb1.c,tb2.d from t_dml_upsert_sub0129_01 tb1 left join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb1.b = 13);
explain (costs off, verbose) insert into t_dml_upsert0129 values(2,2,3) on duplicate key update(c,d)=(select tb1.c,tb2.d from t_dml_upsert_sub0129_01 tb1 left join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb1.b = 13);
select * from t_dml_upsert0129;
explain (costs off, verbose) select tb1.c from t_dml_upsert_sub0129_01 tb1 left join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb2.d = 'd-13';
insert into t_dml_upsert0129 values(3,2,3) on duplicate key update c =(select tb1.c from t_dml_upsert_sub0129_01 tb1 left join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb2.d = 'd-13');
explain (costs off, verbose) insert into t_dml_upsert0129 values(2,2,3) on duplicate key update c =(select tb1.c from t_dml_upsert_sub0129_01 tb1 left join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb2.d = 'd-13');
select * from t_dml_upsert0129;

--CTE with子句 多表关联查询
explain (costs off, verbose) with tmptb(a,c,d) as (select * from t_dml_upsert_sub0129_01 tb1 ,t_dml_upsert_sub0129_02 tb2 where tb1.b=tb2.b) select c from tmptb where a=4;
insert into t_dml_upsert0129 values (4,4) on duplicate key update c = (with tmptb(a,c,d) as (select * from t_dml_upsert_sub0129_01 tb1 ,t_dml_upsert_sub0129_02 tb2 where tb1.b=tb2.b) select c from tmptb where a=4);
select * from t_dml_upsert0129;
explain (costs off, verbose) insert into t_dml_upsert0129 values (4,4) on duplicate key update c = (with tmptb(a,c,d) as (select * from t_dml_upsert_sub0129_01 tb1 ,t_dml_upsert_sub0129_02 tb2 where tb1.b=tb2.b) select c from tmptb where a=4);

--except 多表关联查询
explain (costs off, verbose) select c from t_dml_upsert_sub0129_01 where b = (select b from t_dml_upsert_sub0129_01 except select b from t_dml_upsert_sub0129_02 order by b limit 1);
insert into t_dml_upsert0129 values (3,3) on duplicate key update c = (select c from t_dml_upsert_sub0129_01 where b = (select b from t_dml_upsert_sub0129_01 except select b from t_dml_upsert_sub0129_02 order by b limit 1)) ;
select * from t_dml_upsert0129;
explain (costs off, verbose) insert into t_dml_upsert0129 values (3,3) on duplicate key update c = (select c from t_dml_upsert_sub0129_01 where b = (select b from t_dml_upsert_sub0129_01 except select b from t_dml_upsert_sub0129_02 order by b limit 1)) ;

--excluded;join; muilt-set/single-set均支持
insert into t_dml_upsert0129 values(2,2,3) on duplicate key update(c,d)=(select tb1.c,tb2.d from t_dml_upsert_sub0129_01 tb1 join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb1.b = excluded.b);
select * from t_dml_upsert0129;
explain (costs off, verbose) insert into t_dml_upsert0129 values(2,2,3) on duplicate key update(c,d)=(select tb1.c,tb2.d from t_dml_upsert_sub0129_01 tb1 join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb1.b = excluded.b);
insert into t_dml_upsert0129 values(2,2,3) on duplicate key update c =(select tb1.c from t_dml_upsert_sub0129_01 tb1 join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb2.d = 'd-'||(excluded.b+excluded.c)*2);
select * from t_dml_upsert0129;
explain (costs off, verbose) insert into t_dml_upsert0129 values(2,2,3) on duplicate key update c =(select tb1.c from t_dml_upsert_sub0129_01 tb1 join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb2.d = 'd-'||(excluded.b+excluded.c)*2);

--excluded;right join; muilt-set/single-set均支持
insert into t_dml_upsert0129 values(3,2,3) on duplicate key update(c,d)=(select tb1.c,tb2.d from t_dml_upsert_sub0129_01 tb1 right join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb1.b = excluded.a);
select * from t_dml_upsert0129;
explain (costs off, verbose) insert into t_dml_upsert0129 values(3,2,3) on duplicate key update(c,d)=(select tb1.c,tb2.d from t_dml_upsert_sub0129_01 tb1 right join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb1.b = excluded.a);
insert into t_dml_upsert0129 values(3,2,3) on duplicate key update c =(select tb1.c from t_dml_upsert_sub0129_01 tb1 right join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb2.d = 'd-'||(excluded.b+excluded.c)*2);
select * from t_dml_upsert0129;
explain (costs off, verbose) insert into t_dml_upsert0129 values(3,2,3) on duplicate key update c =(select tb1.c from t_dml_upsert_sub0129_01 tb1 right join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb2.d = 'd-'||(excluded.b+excluded.c)*2);

--excluded;left join; muilt-set/single-set均支持
explain (costs off, verbose) select tb1.c,tb2.d from t_dml_upsert_sub0129_01 tb1 left join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb1.b = 13;
insert into t_dml_upsert0129 values(2,2,3) on duplicate key update(c,d)=(select tb1.c,tb2.d from t_dml_upsert_sub0129_01 tb1 left join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb1.b = (excluded.b+excluded.c)*2 + excluded.c);
explain (costs off, verbose) insert into t_dml_upsert0129 values(2,2,3) on duplicate key update(c,d)=(select tb1.c,tb2.d from t_dml_upsert_sub0129_01 tb1 left join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb1.b = (excluded.b+excluded.c)*2 + excluded.c);
select * from t_dml_upsert0129;
explain (costs off, verbose) select tb1.c from t_dml_upsert_sub0129_01 tb1 left join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb2.d = 'd-13';
insert into t_dml_upsert0129 values(2,2,3) on duplicate key update c =(select tb1.c from t_dml_upsert_sub0129_01 tb1 left join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb2.d = 'd-'||(excluded.b+excluded.c)*2 + excluded.c);
explain (costs off, verbose) insert into t_dml_upsert0129 values(2,2,3) on duplicate key update c =(select tb1.c from t_dml_upsert_sub0129_01 tb1 left join t_dml_upsert_sub0129_02 tb2 on tb1.b=tb2.b where tb2.d = 'd-'||(excluded.b+excluded.c)*2 + excluded.c);
select * from t_dml_upsert0129;

--excluded;CTE with子句 多表关联查询
insert into t_dml_upsert0129 values (4,4) on duplicate key update c = (with tmptb(a,c,d) as (select * from t_dml_upsert_sub0129_01 tb1 ,t_dml_upsert_sub0129_02 tb2 where tb1.b=tb2.b) select c from tmptb where a=excluded.a);
select * from t_dml_upsert0129;
explain (costs off, verbose) insert into t_dml_upsert0129 values (4,4) on duplicate key update c = (with tmptb(a,c,d) as (select * from t_dml_upsert_sub0129_01 tb1 ,t_dml_upsert_sub0129_02 tb2 where tb1.b=tb2.b) select c from tmptb where a=excluded.a);

--excluded;except 多表关联查询
insert into t_dml_upsert0129 values (3,3) on duplicate key update c = (select c from t_dml_upsert_sub0129_01 where b in (select b from t_dml_upsert_sub0129_01 except select b from t_dml_upsert_sub0129_02 order by b) and b > excluded.b*6 limit 1) ;
select * from t_dml_upsert0129;
explain (costs off, verbose) insert into t_dml_upsert0129 values (3,3) on duplicate key update c = (select c from t_dml_upsert_sub0129_01 where b in (select b from t_dml_upsert_sub0129_01 except select b from t_dml_upsert_sub0129_02 order by b) and b>excluded.b*6 limit 1) ;

--函数及表达式
explain (costs off, verbose) insert into t_dml_upsert0129 values (3,3) on duplicate key update (c) =(select excluded.a in (select b from t_dml_upsert_sub0129_01));
insert into t_dml_upsert0129 values (3,3) on duplicate key update (c) =(select excluded.a in (select b from t_dml_upsert_sub0129_01));
select * from t_dml_upsert0129;
explain (costs off, verbose) insert into t_dml_upsert0129 values (3,3) on duplicate key update (c) =(select excluded.a not in (select b from t_dml_upsert_sub0129_01));
insert into t_dml_upsert0129 values (3,3) on duplicate key update (c) =(select excluded.a not in (select b from t_dml_upsert_sub0129_01));
select * from t_dml_upsert0129;
explain (costs off, verbose) insert into t_dml_upsert0129 values (3,3) on duplicate key update (c) =(select min(t_dml_upsert_sub0129_02.b) from t_dml_upsert_sub0129_01 left join t_dml_upsert_sub0129_02 on t_dml_upsert_sub0129_01.b=t_dml_upsert_sub0129_02.b-1 where t_dml_upsert_sub0129_01.b in (select b from t_dml_upsert0129));
insert into t_dml_upsert0129 values (3,3) on duplicate key update (c) =(select min(t_dml_upsert_sub0129_02.b) from t_dml_upsert_sub0129_01 left join t_dml_upsert_sub0129_02 on t_dml_upsert_sub0129_01.b=t_dml_upsert_sub0129_02.b-1 where t_dml_upsert_sub0129_01.b in (select b from t_dml_upsert0129));
select * from t_dml_upsert0129;

--测试数据清理
drop table if exists t_dml_upsert0129;
drop table if exists t_dml_upsert_sub0129_01;
drop table if exists t_dml_upsert_sub0129_02;
