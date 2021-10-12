-- @testpoint:order by条件
drop table if exists t2;
create table t2 (a int,b char(10));
select a,b,trim('2' from '2342') from t2 order by concat(a,b),a;
drop table t2;
