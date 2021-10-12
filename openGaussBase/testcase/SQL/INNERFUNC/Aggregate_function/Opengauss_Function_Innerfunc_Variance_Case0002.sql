-- @testpoint:  函数variance()，对于浮点类型的输入返回double precision类型，其他输入返回numeric类型，入参为无效值时，合理报错

drop table if exists table_test;
create table table_test(
col_1 numeric(10,4),
col_2 int,
col_3 int,
col_4 varchar
);
insert into table_test values(123456.123,234,'','张三'),
(123454.12354,256,null,'李四'),
(123466.456,234,null,'xiaoming'),
(123433.123,234,null,'laozhang');

--入参为字符串
select variance(col_4) from table_test;
drop table if exists table_test;

--入参为时间类型
drop table if exists table_test;
create table table_test(col_1 date,col_2 time,col_3 timestamp,col_4 smalldatetime);
insert into table_test values ('12-10-2010','21:21:21','2010-12-12','2003-04-12 04:05:06'),
('12-10-2023','21:21:21','2010-12-12','2003-04-12 04:05:06');
select variance(col_1) from table_test;
drop table if exists table_test;