-- @testpoint: 输入为字符类型（合理报错）

drop table if exists atan2_test_02;
create table atan2_test_02(f1 char(50),f2 nchar(100),f3 varchar(332),f4 nvarchar2(100),f5 nvarchar2(200),f6 int);
insert into atan2_test_02(f1,f2,f3,f4,f5,f6) values ('aa','bb','cc','dd','ee','123');

select atan2(f5,f4) from atan2_test_02;
select atan2(f4,f3) from atan2_test_02;
select atan2(f3,f2) from atan2_test_02;
select atan2(f2,f1) from atan2_test_02;
select atan2(f1,f5) from atan2_test_02;
drop table if exists atan2_test_02;