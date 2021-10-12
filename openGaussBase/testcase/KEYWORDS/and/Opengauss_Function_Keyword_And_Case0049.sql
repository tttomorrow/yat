-- @testpoint: 定义和使用列时不使用and,结合where条件使用and
drop table if exists t_student cascade;
create table t_student (stu_name char(20),stu_age int,sex char(10),score int,address char(10));
insert into t_student values('zhangsan',18,'boy'),('lisi',25,'boy'),('wangwu',28,'girl'),('zhaosi',35,'boy');
select * from t_student where stu_age>25 and stu_age<30;
drop table if exists t_student;