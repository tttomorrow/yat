-- @testpoint: 有效值验证
drop table if exists t_function_1;
create table t_function_1(f0 bigint, f1 int, f2 double precision, f3 char(10), f4 varchar(10), f5 number(10,6), f6 date, f7 timestamp);
insert into t_function_1(f0, f1, f2, f3, f4, f5, f6, f7) values(null, null, 2.22, '5', 'test', 87.223, null, '2018-02-28 12:13:14.456');
insert into t_function_1(f0, f1, f2, f3, f4, f5, f6, f7) values(1, 2, 1.112233, '3', 'nebulaisok', 998.22222, '2018-01-31 12:13:14', null);
commit;
select avg(f0),avg(f1),avg(f2),avg(f5) from t_function_1;
select avg(f3) from t_function_1;
select sum(f0), min(f1), count(f2), avg(f5), max(f1) from t_function_1;
drop table if exists t_function_1;