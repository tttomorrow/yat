--  @testpoint:定义和使用列时不使用as,给列起别名
drop table if exists test_as_014;
create table test_as_014 (stu_name char(20),stu_age int,sex char(10),score int,address char(10));
insert into  test_as_014 values('zhangsan',18,'boy'),('lisi',25,'boy'),('wangwu',28,'girl');
select stu_name as name,stu_age as age,sex as stu_sex from test_as_014;
drop table test_as_014;