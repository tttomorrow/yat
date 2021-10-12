-- @testpoint: 定义和使用authid列带双引号
drop table if exists test_authid_002;
create table test_authid_002 ("authid" char(20),stu_age int,sex char(10),score int,address char(10));
insert into  test_authid_002 ("authid")values('zhangsan');
select * from  test_authid_002;
drop table if exists test_authid_002;