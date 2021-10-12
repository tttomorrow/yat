-- @testpoint: 函数corr(Y, X)，相关系数

drop table if exists table_test;
create table table_test(id integer,
name varchar(10),
age integer,
height decimal(5,2),
hobbies text,
tel bigint
);
select corr(tel, height)from  table_test where id <5;
select corr(height, id)from  table_test where id <5;
select corr(age, id)from  table_test where id <9;
drop table table_test;