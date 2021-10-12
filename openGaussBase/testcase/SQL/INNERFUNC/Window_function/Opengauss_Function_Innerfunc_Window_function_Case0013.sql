-- @testpoint: NTH_VALUE(value any, nth integer)，函数返回该组内的第nth行作为结果。若该行不存在，则默认返回NULL

create table user_sales_table ( user_name varchar ( 10 ), pay_amount int );
insert into user_sales_table
values
	('A',50),('A',100),('B',250),('B',20),('B',30),
	('C',100),('C',180),('D',120),('D',25),('E',408),
	('F',162),('F',356),('F',128),('F',195),('G',372),
	('G',291),('G',347),('G',207),('G',412),('H',234),
	('H',404),('I',377),('I',295),('I',374),('J',311);

--入参1为字段名，入参2为数字
select user_name, pay_amount, nth_value(pay_amount,5) over ( partition by user_name order by pay_amount desc ) from user_sales_table;
select user_name, pay_amount, nth_value(pay_amount,26) over ( partition by user_name order by pay_amount desc ) from user_sales_table;

--入参1为数字，入参2为字段名
select user_name, pay_amount, nth_value(3,pay_amount) over ( partition by user_name order by pay_amount desc ) from user_sales_table ;

--清理环境
drop table user_sales_table;


