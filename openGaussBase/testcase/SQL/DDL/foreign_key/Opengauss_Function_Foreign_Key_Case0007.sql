-- @testpoint: 测试外键表对临时表的支持情况，合理报错

--测试点1：父表为临时表（会话级本地临时表），子表为行存表
drop table if exists student;
drop table if exists teacher;
create temporary table teacher
(
    t_id int primary key,
    t_name char(16) not null
) On Commit Preserve Rows;
create table student
(
    s_id int primary key,
    t_id int references teacher (t_id) on update cascade on delete set null
);
drop table if exists student;
drop table if exists teacher;
--测试点2：父表为行存表，子表为临时表（事务级本地临时表）
START TRANSACTION;
drop table if exists student;
drop table if exists teacher;
create table teacher
(
    t_id int primary key,
    t_name char(16) not null
);
create temporary table student
(
    s_id int primary key,
    t_id int references teacher (t_id) on update cascade on delete set null
) On Commit Delete Rows;
drop table if exists student;
drop table if exists teacher;
END;
--测试点3：父表为临时表，子表为临时表
--3.1 父表为事务级本地临时表，子表为事务级本地临时表
START TRANSACTION;
drop table if exists student;
drop table if exists teacher;
create temporary table teacher
(
    t_id int primary key,
    t_name char(16) not null
) On Commit Delete Rows;
create temporary table student
(
    s_id int primary key,
    t_id int references teacher (t_id) on update CASCADE on delete set null
) On Commit Delete Rows;
insert into teacher values (2017100001, '张老师');
insert into student values (2017200001, 2017100001);
select * from student;
update teacher set t_id = 2018100001 where t_id = 2017100001;
select * from student;
delete from teacher where t_id = 2018100001;
select * from student;
drop table if exists student;
drop table if exists teacher;
END;
--3.2 父表为会话级本地临时表，子表为会话级本地临时表
drop table if exists student;
drop table if exists teacher;
create temporary table teacher
(
    t_id int primary key,
    t_name char(16) not null
) On Commit Preserve Rows;
create temporary table student
(
    s_id int primary key,
    t_id int references teacher (t_id) on update no action on delete restrict
) On Commit Preserve Rows;
insert into teacher values (2017100001, '张老师');
insert into student values (2017200001, 2017100001);
select * from student;
update teacher set t_id = 2018100001 where t_id = 2017100001;
select * from student;
delete from teacher where t_id = 2017100001;
select * from student;
drop table if exists student;
drop table if exists teacher;
--3.3 父表为事务级临时表，子表为会话级临时表
drop table if exists student;
drop table if exists teacher;
start TRANSACTION;
create temporary table teacher
(
    t_id int primary key,
    t_name char(16) not null
) On Commit Delete Rows;
create temporary table student
(
    s_id int primary key,
    t_id int references teacher (t_id) on update set null on delete no action
) On Commit Preserve Rows;
insert into teacher values (2017100001, '张老师');
insert into teacher values (2017100002, '李老师');
insert into student values (2017200001, 2017100001);
insert into student values (2017200002, 2017100002);
select * from student;
update teacher set t_id = 2018100001 where t_id = 2017100001;
select * from student;
delete from teacher where t_id = 2017100002;
select * from student;
drop table if exists student;
drop table if exists teacher;
end;
--3.4 父表为会话级临时表，子表为事务级临时表
drop table if exists student;
drop table if exists teacher;
start TRANSACTION;
create temporary table teacher
(
    t_id int primary key,
    t_name char(16) not null
) On Commit Preserve Rows;
create temporary table student
(
    s_id int primary key,
    t_id int default 2017100003 references teacher (t_id) on update set default on delete set default
) On Commit Delete Rows;
insert into teacher values (2017100001, '张老师');
insert into teacher values (2017100002, '李老师');
insert into teacher values (2017100003, '田老师');
insert into student values (2017200001, 2017100001);
insert into student values (2017200002, 2017100002);
select * from student;
update teacher set t_id = 2018100001 where t_id = 2017100001;
select * from student;
delete from teacher where t_id = 2017100002;
select * from student;
drop table if exists student;
drop table if exists teacher;
end;
--测试点4：父表，子表是同一个表
--4.1 事务级本地临时表
drop table if exists student;
start TRANSACTION;
create temporary table student
(
    s_id int primary key,
    s_name varchar not null,
    m_id int references student (s_id) on update cascade on delete set null
) On Commit Delete Rows;
insert into student values (2017200001, '张三', 2017200001);
insert into student values (2017200002, '李四', 2017200001);
insert into student values (2017200003, '王二', 2017200002);
select * from student;
update student set s_id = 2018200001 where s_id = 2017200001;
select * from student;
delete student where s_id = 2017200002;
select * from student;
drop table if exists student;
end;
--4.2 会话级本地临时表
drop table if exists student;
create temporary table student
(
    s_id int primary key,
    s_name varchar not null,
    m_id int references student (s_id) on update cascade on delete set null
) On Commit Preserve Rows;
insert into student values (2017200001, '张三', 2017200001);
insert into student values (2017200002, '李四', 2017200001);
insert into student values (2017200003, '王二', 2017200002);
select * from student;
update student set s_id = 2018200001 where s_id = 2017200001;
select * from student;
delete student where s_id = 2017200002;
select * from student;
drop table if exists student;
drop table if exists teacher;
