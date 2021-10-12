-- @testpoint: 字符处理函数trim，函数作为order by条件项

drop table if exists t2;
create table t2 (a int,b char(10));
insert into t2 values(10,'abc');
insert into t2 values(20,'abc');
insert into t2 values(20,'abc');
insert into t2 values(82,'cd');
insert into t2 values(43,'cd');
insert into t2 values(89,'abc');
select a,b,trim('2' from '2342') from t2 order by trim('2' from '2342'),a;
drop table t2;
