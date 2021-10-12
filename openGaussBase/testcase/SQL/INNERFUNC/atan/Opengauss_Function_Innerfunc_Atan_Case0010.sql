-- @testpoint: 结合关键字的使用测试
drop table if exists atan_test_01;
create table atan_test_01(f1 int,f2 bigint,f3 integer,f4 binary_integer,f5 bigint,
                          f6 real,f7 float,f8 binary_double,f9 decimal,f10 number,f11 numeric);
insert into atan_test_01(f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11) values(11,22,33,44,55,11.1,22.2,33.3,44.4,55.5,66.6);
insert into atan_test_01(f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11) values(66,77,88,99,00,'11.1','22.2','33.3','44.4','55.5','66.6');
drop table if exists atan_test_02;
create table atan_test_02(f1 char(50),f2 nchar(100),f3 varchar(332),f4 nvarchar2(100),f5 nvarchar2(200),f6 int);
insert into atan_test_02(f1,f2,f3,f4,f5,f6) values ('aa','bb','cc','dd','ee','123');
select distinct * from atan_test_01 where exists(select cast(atan(f6) as number(5,2)) from atan_test_01);
select distinct f2,f3 from atan_test_01 where exists (select atan(f2) from atan_test_01) order by 1,2;
select distinct cast(atan(1+1-3) as number(5,2)),cast(atan(f2)+atan(f3) as number(5,2)) from atan_test_01;
select distinct T1.f1,T1.f2 from atan_test_01 T1 inner join atan_test_02 T2 on atan(T1.f2) = atan(T2.f6);
drop table if exists atan_test_01;
drop table if exists atan_test_02;