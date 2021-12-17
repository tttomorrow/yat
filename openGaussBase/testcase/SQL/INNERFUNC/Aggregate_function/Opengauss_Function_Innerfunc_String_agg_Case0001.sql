-- @testpoint: 函数string_agg(expression, delimiter)，将输入值连接成为一个字符串，用分隔符分开

drop table if exists table_test;
create table table_test(id integer,
name varchar(10),
age integer,
height decimal(5,2),
hobbies text,
tel bigint
);
insert into table_test values(1, '张三', null, 156.23, 'sings', 12355551895),
(7, '李四', null, 146.45, 'read books', 12866661265),
(3, '李华', null, 160.55, 'Dancing', 11822220366),
(5, '赵六', null, 170.55, 'Playing games', 13344443322);

select string_agg(name, 1) from table_test;
select string_agg(name, 'yyuu') from table_test;
select string_agg(name, '、') from table_test;
select string_agg(tel, '@') from table_test;
select string_agg(tel, '这是分隔符') from table_test;
select string_agg('123', '、') from table_test;
drop table table_test;