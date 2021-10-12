-- @testpoint: 使用max查询某一列的最大值
drop table if exists t_student;
create table t_student (stu_name char(20),stu_age int,sex char(10),score int,address char(10));
insert into t_student values('zhangsan',18,'boy'),('lisi',25,'boy'),('wangwu',28,'girl'),('zhaosi',35,'boy');
select max(stu_age) from t_student;
--清理环境
drop table if exists t_student cascade;