-- @testpoint: 数字操作函数，正切函数，函数表达式

drop table if exists tan_T1;
create table tan_T1(f1 int,f2 bigint,f3 integer,f4 binary_integer,f5 bigint);
insert into tan_T1(f1,f2,f3,f4,f5) values(0,22,33,44,55);
select tan(COS(180 * 3.14159265359/180)) from sys_dummy;
select tan(exp(3)) from sys_dummy;
select avg(tan(0-f1))from tan_T1;
drop table if exists tan_T1;