--  @testpoint:定义和使用as列带反引号,应该报错
drop table if exists test_as_003;
create table test_as_003(`as` char(20),stu_age int,sex char(10),score int,address char(10));