-- @testpoint: 函数regr_syy(Y, X)，sum(Y^2) - sum(Y)^2/N（因变量的"平方和"）

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