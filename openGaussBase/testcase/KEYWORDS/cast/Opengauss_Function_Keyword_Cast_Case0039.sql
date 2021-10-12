--  @testpoint:验证cast函数是否能够将日期类型转为字符型
drop table if exists TEST1;
create table TEST1( riqi date);
insert into TEST1 values(to_date('2018-08-15 17:27:39','yyyy-mm-dd hh24:mi:ss'));
select cast(riqi as signed char) from TEST1;
drop table  TEST1;