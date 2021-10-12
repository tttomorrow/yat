-- @testpoint: 函数regr_count，两个表达式都不为NULL的输入行数

drop table if exists table_test;
create table table_test(id integer,
name varchar(10),
age integer,
height decimal(5,2),
hobbies text,
tel bigint
);
select regr_count(tel, height)from  table_test;
select regr_count(height, id)from  table_test where id <5;
select regr_count(age, id)from  table_test where id <9;
drop table table_test;