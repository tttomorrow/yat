-- @testpoint: 函数min(expression)，所有输入行中expression的最大值，入参为无效值时，合理报错

drop table if exists table_test;
create table table_test(
id integer,
name varchar(10),
age integer,
height dec(5,2),
hobbies text,
tel bigint,
enrollment_time date
);

--当入参有两个参数时
select min(id,tel) from table_test;
drop table if exists table_test;