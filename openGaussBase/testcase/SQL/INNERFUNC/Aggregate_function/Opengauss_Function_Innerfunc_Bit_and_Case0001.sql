-- @testpoint: 函数bit_and(expression)，所有非NULL输入值的按位与(AND)，如果全部输入值皆为NULL，那么结果也为NULL

drop table if exists table_test;
create table table_test(id integer,
name varchar(10),
age integer,
height decimal(5,2),
hobbies text, tel bigint
);
select bit_and(id)from  table_test where id <5;
select bit_and(height)from  table_test where id <5;
select bit_and(age)from  table_test where id <9;
select bit_and(tel)from  table_test where id <9;
drop table table_test;