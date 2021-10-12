-- @testpoint: 函数regr_sxx(Y, X),sum(X^2) - sum(X)^2/N （自变量的“平方和”）

drop table if exists table_test;
create table table_test(id integer,
name varchar(10),
age integer,
height decimal(5,2),
hobbies text,
tel bigint
);
select regr_sxx(tel, height)from  table_test;
select regr_sxx(height, id)from  table_test where id <5;
select regr_sxx(age, id)from  table_test where id <9;
drop table table_test;