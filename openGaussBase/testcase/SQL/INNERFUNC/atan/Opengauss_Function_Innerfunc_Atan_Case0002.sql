-- @testpoint: 输入为字符类型（合理报错）

drop table if exists atan_test_02;
create table atan_test_02(f1 char(50),f2 nchar(100),f3 varchar(332),f4 nvarchar2(100),f5 nvarchar2(200),f6 int);
insert into atan_test_02(f1,f2,f3,f4,f5,f6) values ('aa','bb','cc','dd','ee','123');

select atan(f5) from atan_test_02;
select atan(f4) from atan_test_02;
select atan(f3) from atan_test_02;
select atan(f2) from atan_test_02;
select atan(f1) from atan_test_02;
drop table if exists atan_test_02;