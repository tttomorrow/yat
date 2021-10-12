-- @testpoint: 函数bit_or(expression),所有非NULL输入值的按位或(OR)，如果全部输入值皆为NULL，那么结果也为NULL，入参为数无效值，合理报错

drop table if exists table_test;
create table table_test(id integer,
name varchar(10),
age integer,
height decimal(5,2),
hobbies text,
tel bigint
);
select bit_or(name)from  table_test where id <9;
drop table table_test;

