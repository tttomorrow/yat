-- @testpoint: 函数max(expression)，所有输入行中expression的最大值，入参为有效值时

drop table if exists table_test;
create table table_test(id integer,
name varchar(10),
age integer,
height dec(5,2),
hobbies text,
tel bigint,
enrollment_time date
);
insert into table_test values(1, '张三', 12, 156.23, 'sings', 12355551895, '12-10-2010'),
(7, '李四', 15, 146.45, 'read books', 12866661265, '1-9-2012'),
(3, '李华', 18, 160.55, 'Dancing', 11822220366, '1-9-2006'),
(5, '赵六', 18, 170.55, 'Playing games', 13344443322,'1-9-2005');

--当入参为int类型时
select max(id) from table_test;
--当入参为bigint类型时
select max(tel) from table_test;
--当入参为浮点数时
select max(height) from table_test;
--当入参为字符串时
select max(name) from table_test;
select max(hobbies) from table_test;
--当入参为时间类型时
select max(enrollment_time) from table_test;
--入参为数组时
select max(array[[1.1,2.1,3.1],[2,3,4]]) as result;
drop table table_test;

