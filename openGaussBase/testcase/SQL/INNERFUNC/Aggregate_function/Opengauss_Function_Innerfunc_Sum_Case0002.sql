-- @testpoint: 函数sum(expression),所有输入行的expression总和，入参为无效值时，合理报错

drop table if exists table_test;
create table table_test(id integer,
name varchar(10),
age integer,
height dec(5,2),
hobbies text,
tel bigint
);

--当入参为非数值类型时
select sum(name) from table_test;
select sum(hobbies) from table_test;
drop table table_test;