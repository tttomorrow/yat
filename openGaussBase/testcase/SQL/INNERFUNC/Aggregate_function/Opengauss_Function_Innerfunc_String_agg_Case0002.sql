-- @testpoint: 函数string_agg(expression, delimiter)，将输入值连接成为一个字符串，用分隔符分开,入参为无效值时，合理报错

drop table if exists table_test;
create table table_test(id integer,
name varchar(10),
age integer,
height decimal(5,2),
hobbies text,
tel bigint );

--分隔符为不带引号的中文
select string_agg(name, 你好) from table_test;
--分隔符为不带引号的特殊符号
select string_agg(name, #) from table_test;
--输入值为两个参数时
select string_agg(name, id, '、') from table_test;
drop table table_test;