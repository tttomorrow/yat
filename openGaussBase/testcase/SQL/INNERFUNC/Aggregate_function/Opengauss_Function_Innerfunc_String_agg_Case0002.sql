-- @testpoint: 函数string_agg(expression, delimiter)，将输入值连接成为一个字符串，用分隔符分开,入参为无效值时，合理报错

drop table if exists table_test;
create table table_test(id integer,
name varchar(10),
age integer,
height decimal(5,2),
hobbies text,
tel bigint );
insert into table_test values(1, '张三', null, 156.23, 'sings', 12355551895),
(7, '李四', null, 146.45, 'read books', 12866661265),
(3, '李华', null, 160.55, 'Dancing', 11822220366),
(5, '赵六', null, 170.55, 'Playing games', 13344443322);

--分隔符为不带引号的中文
select string_agg(name, 你好) from table_test;
--分隔符为不带引号的特殊符号
select string_agg(name, #) from table_test;
--输入值为两个参数时
select string_agg(name, id, '、') from table_test;
drop table table_test;