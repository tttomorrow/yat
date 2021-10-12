-- @testpoint: 创建列类型是字符类型的列存表
drop table if exists table_2;
create table table_2(a character(10),b  varchar(20))with (ORIENTATION=COLUMN);
insert into table_2 values('zhangxiao'),('zhulin');
insert into table_2 values('张三'),('李四');
select * from table_2;
drop table if exists table_2;