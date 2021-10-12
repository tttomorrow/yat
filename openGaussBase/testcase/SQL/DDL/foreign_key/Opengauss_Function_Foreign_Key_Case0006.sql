-- @testpoint: 测试外键表对列存表的支持情况，合理报错

--测试点1：父表为列存表，子表为行存表
drop table if exists student;
drop table if exists teacher_column;
create table teacher_column
(
    t_id int primary key,
    t_name varchar not null
) with (orientation = column);
create table student
(
    s_id int,
    s_name varchar not null,
    t_id int references teacher_column on update cascade on delete set null
);
drop table if exists student;
drop table if exists teacher_column;
--测试点2：父表为行存表，子表为列存表
drop table if exists student_column;
drop table if exists teacher;
create table teacher
(
    t_id int primary key,
    t_name varchar not null
);
create table student_column
(
    s_id int,
    s_name varchar not null,
    t_id int references teacher on update cascade on delete set null
) with (orientation = column);
drop table if exists student_column;
drop table if exists teacher;
--测试点3：父表为列存表，子表为列存表
drop table if exists student_column;
drop table if exists teacher_column;
create table teacher_column
(
    t_id int primary key,
    t_name varchar not null
) with (orientation = column);
create table student_column
(
    s_id int,
    s_name varchar not null,
    t_id int references teacher_column on update cascade on delete set null
) with (orientation = column);
drop table if exists student_column;
drop table if exists teacher_column;
drop table if exists teacher;
