-- @testpoint: 建表时使用check约束，插入检查约束的边界值，插入19，合理报错

--step1：创建表; expect:成功
drop table if exists t_student;
create table t_student (stu_name char(20),stu_age int check (stu_age>20),sex char(10),score int,address char(10));

--step2：给表插入数据; expect:合理报错
insert into t_student values('lisi',19,'boy',80,'shanxi');

--step4：清理环境; expect:成功
drop table if exists t_student;