-- @testpoint: 函数string_agg(expression, delimiter)，将输入值连接成为一个字符串，用分隔符分开

drop table if exists table_test;
create table table_test(id integer,
name varchar(10),
age integer,
height decimal(5,2),
hobbies text,
tel bigint
);

select string_agg(name, 1) from table_test;
select string_agg(name, 'yyuu') from table_test;
select string_agg(name, '、') from table_test;
select string_agg(tel, '@') from table_test;
select string_agg(tel, '这是分隔符') from table_test;
select string_agg('123', '、') from table_test;
drop table table_test;