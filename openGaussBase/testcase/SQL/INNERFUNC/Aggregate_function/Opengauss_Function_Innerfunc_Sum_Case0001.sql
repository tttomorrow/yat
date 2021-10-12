-- @testpoint: 函数sum(expression),所有输入行的expression总和，入参为有效值时

drop table if exists table_test;
create table table_test(id integer,
name varchar(10),
age integer,
height dec(5,2),
hobbies text,
tel bigint
);

--当入参为int类型时
select sum(id) from table_test;
--当入参为bigint类型时
select sum(tel) from table_test;
--当入参为浮点数时
select sum(height) from table_test;
drop table table_test;