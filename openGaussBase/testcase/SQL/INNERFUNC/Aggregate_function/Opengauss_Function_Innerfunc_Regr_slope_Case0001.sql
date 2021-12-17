-- @testpoint: 函数regr_slope(Y, X),根据所有输入的点(X, Y)按照最小二乘法拟合成一个线性方程， 然后返回该直线的斜率

drop table if exists table_test;
create table table_test(id integer,
name varchar(10),
age integer,
height decimal(5,2),
hobbies text,
tel bigint
);
insert into table_test values(1, '张三', 12, 156.23, 'sings', 12355551895),
(7, '李四', 15, 146.45, 'read books', 12866661265),
(3, '李华', 18, 160.55, 'Dancing', 11822220366),
(5, '赵六', 18, 170.55, 'Playing games', 13344443322);
select regr_slope(tel, height)from  table_test;
select regr_slope(height, id)from  table_test where id <5;
select regr_slope(age, id)from  table_test where id <9;
drop table table_test;