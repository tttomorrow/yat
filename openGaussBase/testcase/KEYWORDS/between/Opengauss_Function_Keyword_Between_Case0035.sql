-- @testpoint: 使用between...and...查询一列的取值范围
drop table if exists t_student;
create table t_student (stu_name char(20),stu_age int,sex char(10),score int,address char(10),id int,enrollment_time date);
insert into t_student values('zhangsan',18,'boy'),('lisi',25,'boy'),('wangwu',28,'girl'),('zhaosi',35,'boy');
select * from t_student where stu_age between 25 and 35;
drop table if exists t_student;