-- @testpoint: 使用committed开启事务隔离级别为读已提交

drop table if exists t_student;
create table t_student (stu_name char(20),stu_age int,sex char(10));
insert into t_student values('zhangsan',18,'boy'),('lisi',25,'boy'),('wangwu',28,'girl');
start transaction isolation level read committed read write;
update t_student set stu_age=21 where stu_name='zhangsan';
commit;
drop table if exists t_student;