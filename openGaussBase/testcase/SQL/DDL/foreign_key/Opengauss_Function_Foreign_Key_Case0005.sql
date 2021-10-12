-- @testpoint: 测试外键约束检查延迟生效，合理报错
--建立外键表，加入推迟检查约束
drop table if exists student;
drop table if exists teacher;
create table teacher
(
    t_id int primary key,
    t_name varchar not null
);
create table student
(
    s_id int,
    s_name varchar not null,
    t_id int REFERENCES teacher deferrable initially deferred
);
--添加数据
--测试推迟检查约束，应当在commit时报错
START TRANSACTION;
update student set s_id = s_id + 1;
COMMIT;
select * from student;
drop table if exists student;
drop table if exists teacher;