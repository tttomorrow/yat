-- @testpoint: 定义as列带引号，使用时不带双引号或反引号，大小写匹配，合理报错
drop table if exists test_as_004;
create table  test_as_004 ("as" char(20),stu_age int,sex char(10),score int,address char(10));
insert into  test_as_004(as) values('lisi');
drop table if exists test_as_004;