--  @testpoint:定义和使用列时不使用add,使用alter…add给表添加字段
drop table if exists t_student;
create table t_student (stu_name char(20),stu_age int,sex char(10));
insert into t_student values('zhangsan',18,'boy'),('lisi',25,'boy'),('wangwu',28,'girl');
alter table t_student add (height int);
select * from t_student;