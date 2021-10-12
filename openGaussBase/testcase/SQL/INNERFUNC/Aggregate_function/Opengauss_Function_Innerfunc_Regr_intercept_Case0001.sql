-- @testpoint: 函数regr_intercept，根据所有输入的点(X, Y)按照最小二乘法拟合成一个线性方程，然后返回该直线的Y轴截距

drop table if exists table_test;
create table table_test(id integer,
name varchar(10),
age integer,
height decimal(5,2),
hobbies text,
tel bigint
);
select regr_intercept(tel, height)from  table_test;
select regr_intercept(height, id)from  table_test where id <5;
select regr_intercept(age, id)from  table_test where id <9;
drop table table_test;