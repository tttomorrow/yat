-- @testpoint: 函数嵌套
drop table if exists atan2_test_01;
create table atan2_test_01(f1 int,f2 bigint,f3 integer,f4 binary_integer,f5 bigint,
                          f6 real,f7 float,f8 binary_double,f9 decimal,f10 number,f11 numeric);
insert into atan2_test_01(f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11) values(11,22,33,44,55,11.1,22.2,33.3,44.4,55.5,66.6);
insert into atan2_test_01(f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11) values(66,77,88,99,00,'11.1','22.2','33.3','44.4','55.5','66.6');
select atan2(atan2(atan2(atan2(atan2(f2,f1),f1),f2),f3),f4),atan2(f3,f5) from atan2_test_01 where atan2(atan2(f2,f6),f3) <> 0;

select atan2(exp(3),exp(9)) from sys_dummy;
select avg(atan2(0-f1,f3+f6))from atan2_test_01;
drop table if exists atan2_test_01;