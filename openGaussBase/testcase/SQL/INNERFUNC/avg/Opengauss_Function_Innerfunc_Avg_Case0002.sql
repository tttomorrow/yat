-- @testpoint: 对其他数据类型求平均值
drop table if exists t_function_1;
create table t_function_1(f0 bigint, f1 int, f2 double precision, f3 char(10), f4 varchar(10), f5 number(10,6), f6 date, f7 timestamp);
insert into t_function_1(f0, f1, f2, f3, f4, f5, f6, f7) values(1, 1, 3.333, '4', '5asdf', 6.666666666, '2018-01-16 12:13:14', '2017-03-30 12:13:14.456');
insert into t_function_1(f0, f1, f2, f3, f4, f5, f6, f7) values(null, null, 2.22, '5', 'test', 87.223, null, '2018-02-28 12:13:14.456');
insert into t_function_1(f0, f1, f2, f3, f4, f5, f6, f7) values(1, 2, 1.112233, '3', 'nebulaisok', 998.22222, '2018-01-31 12:13:14', null);
select * from t_function_1;
select avg(f3) from t_function_1;
select * from t_function_1 order by f3;
drop table if exists t_function_1;