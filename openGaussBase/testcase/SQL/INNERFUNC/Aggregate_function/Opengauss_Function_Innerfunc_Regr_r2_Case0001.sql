-- @testpoint: 函数regr_r2(Y, X),相关系数的平方

drop table if exists table_test;
create table table_test(id integer,
name varchar(10),
age integer,
height decimal(5,2),
hobbies text,
tel bigint
);
select regr_r2(tel, height)from  table_test;
select regr_r2(height, id)from  table_test where id <5;
select regr_r2(age, id)from  table_test where id <9;
drop table table_test;