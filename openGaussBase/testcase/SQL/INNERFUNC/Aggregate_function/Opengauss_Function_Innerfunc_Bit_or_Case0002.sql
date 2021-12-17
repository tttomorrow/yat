-- @testpoint: 函数bit_or(expression),所有非NULL输入值的按位或(OR)，如果全部输入值皆为NULL，那么结果也为NULL，入参为数无效值，合理报错

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
select bit_or(name)from  table_test where id <9;
drop table table_test;

