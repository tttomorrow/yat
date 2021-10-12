-- @testpoint: >all的情况，测试stu_age的边界值
drop table if exists t_student;
create table t_student (stu_name char(20),stu_age int,sex char(10),score int,address char(10),id int,enrollment_time date);
insert into t_student values('zhangsan',18,'boy'),('lisi',25,'boy'),('wangwu',28,'girl'),('zhaosi',35,'boy');
select * from t_student where 18>all(select stu_age from t_student);
drop table if exists t_student;