-- @testpoint: 测试外键的基本操作（建立、更新、删除）

--测试点1：外键的建立
drop table if exists student;
drop table if exists student1;
drop table if exists class;
drop table if exists teacher;
drop table if exists teacher1;
create table class
(
    c_id int primary key,
    c_name varchar not null
);
create table teacher
(
    t_id int primary key,
    t_name varchar not null
);
--1.1 使用create table建立外键
create table student
(
    s_id int primary key,
    s_name varchar not null,
    c_id int,
    t_id int,
    foreign key(c_id) references class(c_id) on update cascade on delete cascade
);
--1.2 使用alter table建立外键
alter table student add constraint fk_student_tid foreign key (t_id) references teacher(t_id) on update cascade on delete cascade;
--测试点2：外键的更新
insert into class values (101, '1年1班');
insert into class values (102, '1年2班');
insert into class values (103, '1年3班');
insert into class values (104, '1年4班');
insert into teacher values (2017100001, '李老师');
insert into teacher values (2017100002, '张老师');
insert into teacher values (2017100003, '陈老师');
insert into teacher values (2017100004, '杨老师');
insert into student values (2017200001, '张三', 101, 2017100001);
insert into student values (2017200002, '李四', 101, 2017100001);
insert into student values (2017200003, '王二', 102, 2017100002);
insert into student values (2017200004, '李明', 103, 2017100003);
insert into student values (2017200005, '吴天', 104, 2017100004);
--2.1 修改父表表名
select * from student;
alter table teacher rename to teacher1;
delete from teacher1 where t_id = 2017100004;
select * from student;
--2.2 修改父表被参照列名
alter table teacher1 rename t_id to t_id1;
update teacher1 set t_id1 = 2018100003 where t_id1 = 2017100003;
select * from student;
--2.3 修改子表表名
alter table student rename to student1;
update class set c_id = 203 where c_id = 103;
select * from student1;
--2.4 修改子表外键列列名
alter table student1 rename c_id to c_id1;
delete from class where c_id = 203;
select * from student1;
--2.5 修改父表被参照列数据类型（同类型）
alter table class alter column c_id type bigint;
update class set c_id = 202 where c_id = 102;
select * from student1;
--2.6 修改父表被参照列数据类型（不同类型）
alter table class alter column c_id type varchar(10);
delete from class where c_id = '202';
select * from student1;
--2.7 修改子表被参照列数据类型（同类型）
alter table student1 alter column t_id type bigint;
update teacher1 set t_id1 = 2018100001 where t_id1 = 2017100001;
select * from student1;
--2.8 修改子表被参照类数据类型（不同类型）
alter table student1 alter column t_id type varchar(10);
delete from teacher1 where t_id1 = 2018100001; 
select * from student1;
drop table if exists student;
drop table if exists student1;
drop table if exists class;
drop table if exists teacher;
drop table if exists teacher1;
--测试点3：外键的删除
drop table if exists student;
drop table if exists teacher;
create table teacher
(
    t_id1 int primary key,
    t_id2 int unique,
    t_id3 int unique
);
create table student
(
    s_id int primary key,
    t_id1 int,
    t_id2 int,
    t_id3 int
);
alter table student add CONSTRAINT fk_student_tid1 foreign key (t_id1) references teacher(t_id1);
alter table student add CONSTRAINT fk_student_tid2 foreign key (t_id2) references teacher(t_id2);
alter table student add CONSTRAINT fk_student_tid3 foreign key (t_id3) references teacher(t_id3);
select conname, convalidated, confupdtype, confdeltype, confmatchtype from PG_CONSTRAINT where conname in ('fk_student_tid1','fk_student_tid2','fk_student_tid3') order by conname asc;
--3.1 删除外键约束
alter table student drop constraint fk_student_tid3;
select conname, convalidated, confupdtype, confdeltype, confmatchtype from PG_CONSTRAINT where conname in ('fk_student_tid1','fk_student_tid2','fk_student_tid3') order by conname asc;
--3.2 删除父表被参照列
alter table teacher drop column t_id2 cascade;
select conname, convalidated, confupdtype, confdeltype, confmatchtype from PG_CONSTRAINT where conname in ('fk_student_tid1','fk_student_tid2','fk_student_tid3');
--3.3 删除子表外键列
alter table student drop column t_id1 cascade;
select conname, convalidated, confrelid, confupdtype, confdeltype, confmatchtype from PG_CONSTRAINT where conname in ('fk_student_tid1','fk_student_tid2','fk_student_tid3');
drop table if exists student;
drop table if exists teacher;
