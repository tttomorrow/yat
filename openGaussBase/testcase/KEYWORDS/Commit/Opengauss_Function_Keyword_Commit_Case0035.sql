-- @testpoint: 修改某一列字段值后，执行commit成功，再使用rollback
drop table if exists t_student;
create table t_student (stu_name char(20),stu_age int,sex char(10));
insert into t_student values('zhangsan',18,'boy'),('lisi',25,'boy'),('wangwu',28,'girl');
start transaction;
update t_student set stu_age=20 where stu_name='zhangsan';
commit;
rollback;
drop table if exists t_student;