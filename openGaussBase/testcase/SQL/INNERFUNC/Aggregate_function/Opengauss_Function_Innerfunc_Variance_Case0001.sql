-- @testpoint:  函数variance()，对于浮点类型的输入返回double precision类型，其他输入返回numeric类型，入参为有效值时

drop table if exists table_test;
create table table_test(
col_1 numeric(10,4),
col_2 int,
col_3 int,
col_4 varchar
);
insert into table_test values(123456.123,234,'','123');
insert into table_test values(123454.12354,256,null,'164');
insert into table_test values(123466.456,234,null,'183');
insert into table_test values(123433.123,234,null,'173');

--入参为浮点数
select variance(col_1) from table_test;
--入参为整数
select variance(col_2) from table_test;
--入参为''/null
select variance(col_3) from table_test;
--入参为字符串（数值型）
select variance(col_4) from table_test;
drop table table_test;