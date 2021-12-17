-- @testpoint: 数字操作函数，正切函数，有效边界值


drop table if exists tan_T1;
create table tan_T1(f1 int,f2 bigint,f3 integer,f4 binary_integer,f5 bigint);
insert into tan_T1(f1,f2,f3,f4,f5) values(0,22,33,44,55);
select tan(cast(-9223372036854775808 as bigint)),tan(cast(9223372036854775807 as bigint)) from sys_dummy;
select tan(cast(-2147483648 as integer)),tan(cast(2147483647 as integer)) from sys_dummy;
select tan(cast(1.0E-127 as decimal)),tan(cast(1.0E-128 as decimal)) from sys_dummy;
select tan(cast(0 as char(1))),tan(cast(0 as char(8000)))from sys_dummy;
drop table if exists tan_T1;