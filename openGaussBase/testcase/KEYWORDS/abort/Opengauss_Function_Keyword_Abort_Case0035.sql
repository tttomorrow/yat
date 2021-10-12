-- @testpoint: 修改字段值后，使用abort回滚
drop table if exists t_student;
create table t_student (stu_name char(20),stu_age int,sex char(10));
insert into t_student values('zhangsan',18,'boy'),('lisi',25,'boy'),('wangwu',28,'girl');
start transaction;
update t_student set stu_age=30 where stu_name='zhangsan';
select * from t_student;
abort;
drop table if exists t_student;