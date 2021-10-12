-- @testpoint: 测试不同外键约束等级下的insert、update和delete情况，合理报错
--             测试系统表PG_CONSTRAINT对不同外键约束等级

--建立外键表
drop table if exists student;
drop table if exists class;
drop table if exists teacher;
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
create table student
(
    s_id int primary key,
    s_name varchar not null,
    c_id int,
    t_id int
);
--添加数据
insert into class values (101, '1年1班');
insert into class values (102, '1年2班');
insert into class values (103, '1年3班');
insert into class values (104, '1年4班');
select * from student;
--增加外键约束
alter table student add constraint fk_student_tid foreign key (t_id) references teacher(t_id) on delete set null on update no action;
alter table student add constraint fk_student_cid foreign key (c_id) references class(c_id) on delete cascade on update restrict;
--测试点1：测试PG_CONSTRAINT表中情况
select conname, convalidated, confupdtype, confdeltype, confmatchtype from PG_CONSTRAINT where confrelid in (select oid from pg_class where relname in ('teacher', 'class')) order by conname;
--测试点2：delete在set null下的情况
select * from student;
--测试点3：delete在cascade下的情况
delete from class where c_id = 102;
select * from student;
--测试点4：update在no action下的情况
select * from student;
--测试点5：update在restrict下的情况
update class set c_id = 203 where c_id = 103;
select * from student;
--外键约束更新
alter table student drop constraint fk_student_tid;
alter table student drop constraint fk_student_cid;
alter table student add constraint fk_student_tid foreign key (t_id) references teacher(t_id) on delete no action on update cascade;
alter table student add constraint fk_student_cid foreign key (c_id) references class(c_id) on delete restrict on update set null;
--测试点6：delete在no action的情况
select * from student;
--测试点7：delete在restrict的情况
delete from class where c_id = 104;
select * from student;
--测试点8：update在cascade的情况
select * from student;
--测试点9：update在set null的情况
update class set c_id = 201 where c_id = 101;
select * from student;
--测试点1：测试PG_CONSTRAINT表中情况
select conname, convalidated, confupdtype, confdeltype, confmatchtype from PG_CONSTRAINT where conname in ('fk_student_tid', 'fk_student_cid') order by conname;
--删除外键表
drop table if exists student;
drop table if exists class;
drop table if exists teacher;
--测试点11：测试update在set default下的情况
create table teacher
(
    t_id int primary key,
    t_name varchar not null
);
create table student
(
    s_id int primary key,
    s_name varchar not null,
    t_id int default 0 references teacher(t_id) on update set default on delete set default
);
insert into teacher values (0, '000');
select * from student;
select * from student;
--测试点10：测试delete在set default下的情况
select * from student;
drop table if exists student cascade;
drop table if exists teacher cascade;
drop table if exists class cascade;
