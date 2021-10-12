-- @testpoint: 函数regr_sxy(Y, X)，sum(X*Y) - sum(X) * sum(Y)/N （自变量和因变量的“乘方积”）

drop table if exists table_test;
create table table_test(id integer,
name varchar(10),
age integer,
height decimal(5,2),
hobbies text,
tel bigint
);
select regr_sxy(tel, height)from  table_test;
select regr_sxy(height, id)from  table_test where id <5;
select regr_sxy(age, id)from  table_test where id <9;
drop table table_test;
