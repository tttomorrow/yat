--  @testpoint:定义和使用authid列带反引号,应该报错
drop table if exists test_authid_003;
create table test_authid_003 (`authid` char(20),stu_age int,sex char(10),score int,address char(10));
insert into test_authid_003 (`authid``)values('zhangsan');
select * from test_authid_003;