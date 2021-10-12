-- @testpoint: 函数min(expression)，所有输入行中expression的最小值，入参为有效值时

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

--当入参为int类型时
select min(id) from table_test;
--当入参为bigint类型时
select min(tel) from table_test;
--当入参为浮点数时
select min(height) from table_test;
--当入参为字符串时
select min(name) from table_test;
select min(hobbies) from table_test;
--当入参为时间类型时
select min(enrollment_time) from table_test;
--入参为数组时
select min(array[[1.1,2.1,3.1],[2,3,4]]) as result;
drop table table_test;