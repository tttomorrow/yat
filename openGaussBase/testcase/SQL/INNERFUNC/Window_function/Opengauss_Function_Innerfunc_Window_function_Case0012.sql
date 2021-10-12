-- @testpoint: LAST_VALUE(value any),描述：LAST_VALUE函数取各组内的最后一个值作为返回结果,入参为无效值时，合理报错

create table user_sales_table ( user_name varchar ( 10 ), pay_amount int );
insert into user_sales_table
values
	('A',50),('A',100),('B',250),('B',20),('B',30),
	('C',100),('C',180),('D',120),('D',25),('E',408),
	('F',162),('F',356),('F',128),('F',195),('G',372),
	('G',291),('G',347),('G',207),('G',412),('H',234),
	('H',404),('I',377),('I',295),('I',374),('J',311);

--入参为字段名
select user_name, pay_amount, last_value(pay_amount) over ( partition by user_name order by pay_amount desc ) from user_sales_table where pay_amount <300;

--入参为数字
select user_name, pay_amount, last_value(15) over ( partition by user_name order by pay_amount desc ) from user_sales_table where pay_amount <300;

--入参为文本，合理报错时
select user_name, pay_amount, last_value('abc') over ( partition by user_name order by pay_amount desc ) from user_sales_table where pay_amount <300;

--清理环境
drop table user_sales_table;