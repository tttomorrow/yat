-- @testpoint: 测试不同父、子表对应下的外键情况，合理报错

drop table if exists student;
drop table if exists teacher;
--测试点1：测试A表主键对应A表外键
--建立外键表
create table student
(
    s_id int primary key,
    s_name varchar not null,
    m_id int references student (s_id) on update cascade on delete set null
);
--添加数据
insert into student values (2017200001, '张三', 2017200001);
insert into student values (2017200002, '李四', 2017200001);
insert into student values (2017200003, '王二', 2017200002);
--测试delete和update结果
select * from student;
update student set s_id = 2018200001 where s_id = 2017200001;
select * from student;
delete student where s_id = 2017200002;
select * from student;
drop table if exists student;
drop table if exists teacher;
--测试点2：测试A表主键对应B表外键，且B表主、外键重合
drop table if exists student;
drop table if exists teacher;
create table teacher
(
    t_id int primary key,
    t_name varchar not null
);
create table student
(
    s_id int primary key references teacher(t_id) on update cascade on delete cascade,
    s_name varchar not null
);
INSERT INTO teacher VALUES (2017100001, '李老师');
INSERT INTO teacher VALUES (2017100002, '张老师');
insert into student values (2017100001, '李明');
insert into student values (2017100002, '张三');
select * from student;
update teacher set t_id = 2018100001 where t_id = 2017100001;
select * from student;
delete from teacher where t_id = 2017100002;
select * from student;
drop table if exists student;
drop table if exists teacher;
--测试点3：A表1个主键对应B表1个外键
--已在其它用例中覆盖
--测试点4：A表1个主键对应B表1个外键，B表1个主键对应C表一个外键
drop table if exists student_backup;
drop table if exists student;
drop table if exists teacher;
create table teacher
(
    t_id int primary key,
    t_name varchar not null
);
create table student
(
    s_id int primary key,
    s_name varchar,
    t_id int unique references teacher(t_id) on update set null on delete cascade
);
create table student_backup
(
    s_id1 int references student(s_id),
    s_name1 varchar,
    t_id1 int references student(t_id) on update cascade on delete no action
);
insert into teacher values(2017100001, '李老师');
insert into teacher values(2017100002, '张老师');
insert into student values(2017200001, '张三', 2017100001);
insert into student values(2017200002, '张三', 2017100002);
insert into student_backup values(2017200001, '张三', 2017100001);
insert into student_backup values(2017200002, '张三', 2017100002);
select * from student;
select * from student_backup;
update teacher set t_id = 2018100001 where t_id = 2017100001;
select * from student;
select * from student_backup;
delete from teacher where t_id = 2017100002;
select * from student;
select * from student_backup;
drop table if exists student_backup;
drop table if exists student;
drop table if exists teacher;
--测试点5：测试A表1个主键对应B表多个外键
--建立外键表
create table teacher
(
    t_id int primary key,
    t_name varchar not null
);
create table student
(
    s_id int,
    s_name varchar not null,
    yuwen_t_id int REFERENCES teacher on update cascade on delete set null,
    shuxue_t_id int REFERENCES teacher on update cascade on delete set null,
    yingyu_t_id int REFERENCES teacher on update cascade on delete set null
);
--添加数据
INSERT INTO teacher VALUES (2017100001, '李老师');
INSERT INTO teacher VALUES (2017100002, '陈老师');
INSERT INTO teacher VALUES (2017100003, '张老师');
INSERT INTO student VALUES (2017200001, '张三', 2017100001, null, null);
INSERT INTO student VALUES (2017200002, '李四', 2017100002, 2017100002, null);
INSERT INTO student VALUES (2017200003, '王二', 2017100003, 2017100003, 2017100003);
--检查外键情况
SELECT * FROM student;
update teacher set t_id = 2018100003 where t_id = 2017100003;
SELECT * FROM student;
DELETE FROM teacher WHERE t_id = 2018100003;
SELECT * FROM student;
drop table if exists student;
drop table if exists teacher;
--测试点6：A表1个主键、B表1个主键分别对应C表2个外键
--已在其它用例中覆盖

--测试点7：测试A表主键多个字段对应B表多个字段主键
--建立外键表
create table teacher
(
    t_id int,
    t_oid int,
    t_name varchar not null,
    primary key (t_id, t_oid)
);
create table student
(
    s_id int primary key,
    s_name varchar not null,
    t_id int,
    t_oid int,
    CONSTRAINT FK_student_1 FOREIGN KEY (t_id, t_oid) REFERENCES teacher on update cascade on delete set null
);
--插入数据
insert into teacher values (2017100001, 1, '张老师');
insert into teacher values (2017100002, 2, '李老师');
insert into teacher values (2017100003, 3, '陈老师');
--测试插入情况，只有主键全部字段都存在才能成功插入
--应当插入应当执行成功
insert into student values (2017200001, '王二', 2017100001, 1);
insert into student values (2017200002, '张三', 2017100001, 1);
insert into student values (2017200003, '吴五', 2017100004, null);
select * from student;
--外键约束中加入match full限制
delete from student where s_id = 2017200003;
alter table student drop constraint FK_student_1;
alter table student add constraint FK_student_2 FOREIGN KEY (t_id, t_oid) REFERENCES teacher MATCH FULL on update cascade on delete set null;
--以下插入应当执行失败
insert into student values (2017200004, '陈一', 2017100002, 3);
insert into student values (2017200005, '李四', 2017100003, null);
--测试update和delete情况
select * from student;
update teacher set t_id = 2018100001 where t_id = 2017100001;
select * from student;
delete from teacher where t_oid = 1;
select * from student;
drop table if exists student;
drop table if exists teacher;
