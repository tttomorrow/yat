-- @testpoint: 字符处理函数trim，函数作为having条件项

drop table if exists t2;
create table t2 (a int,b char(10));
insert into t2 values(10,'abc');
insert into t2 values(20,'abc');
insert into t2 values(20,'abc');
insert into t2 values(82,'cd');
insert into t2 values(43,'cd');
insert into t2 values(89,'abc');
select sum(a),b from t2 group by b having trim('2' from '2342')='34' order by 1,2;
drop table if exists t2;

