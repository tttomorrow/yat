-- @testpoint: 测试外键表对不同数据类型支持情况

--测试点1：数值类型
drop table if exists student;
drop table if exists teacher;
create table teacher
(
    t_id1 tinyint primary key,
    t_id2 smallint unique,
    t_id3 integer unique,
    t_id4 bigint unique
);
create table student
(
    s_id int primary key,
    t_id1 int1 references teacher(t_id1) on update cascade on delete set null,
    t_id2 int2 references teacher(t_id2) on update cascade on delete set null,
    t_id3 int4 references teacher(t_id3) on update cascade on delete set null,
    t_id4 int8 references teacher(t_id4) on update cascade on delete set null
);
insert into teacher values (254, 32766, 2147483646, 9223372036854775806);
insert into student values (1, 254, 32766, 2147483646, 9223372036854775806);
select * from student;
update teacher set t_id1 = 253 where t_id1 = 254;
select * from student;
delete from teacher where t_id2 = 32766;
select * from student;
drop table if exists student;
drop table if exists teacher;
--测试点2：布尔类型
drop table if exists student;
drop table if exists teacher;
create table teacher
(
    t_id boolean primary key,
    t_name varchar not null
);
create table student
(
    s_id int primary key,
    t_id boolean references teacher(t_id) on update cascade on delete set null
);
insert into teacher values (false, '王老师');
insert into teacher values (true, '张老师');
insert into student values (1, false);
insert into student values (2, true);
select * from student;
delete from teacher where t_id = true;
select * from student;
update teacher set t_id = true where t_id = false;
select * from student;
drop table if exists student;
drop table if exists teacher;
--测试点3：字符类型
drop table if exists student;
drop table if exists teacher;
create table teacher
(
    t_id1 char(10) primary key,
    t_id2 varchar(10) unique,
    t_id3 nvarchar2(10) unique,
    t_id4 clob unique,
    t_name varchar not null
);
create table student
(
    s_id int primary key,
    t_id1 character(10) references teacher(t_id1) on update cascade on delete set null,
    t_id2 character varying(10) references teacher(t_id2) on update cascade on delete set null,
    t_id3 varchar2(10) references teacher(t_id3) on update cascade on delete set null,
    t_id4 text references teacher(t_id4) on update cascade on delete set null,
    s_name varchar not null
);
insert into teacher values ('aaa1', 'bbb1', 'ccc1', 'ddd1', '王老师');
insert into teacher values ('aaa2', 'bbb2', 'ccc2', 'ddd2', '张老师');
insert into student values (1, 'aaa1', 'bbb1', 'ccc1', 'ddd1', '李四');
insert into student values (2, 'aaa2', 'bbb2', 'ccc2', 'ddd2', '张三');
select * from student;
delete from teacher where t_id1 = 'aaa1';
select * from student;
update teacher set t_id2 = 'bbb3' where t_id2 = 'bbb2';
select * from student;
drop table if exists student;
drop table if exists teacher;
--测试点4：二进制类型
drop table if exists student;
drop table if exists teacher;
create table teacher
(
    t_id1 blob primary key,
    t_id2 raw unique,
    t_name varchar not null
);
create table student
(
    s_id int primary key,
    t_id1 blob references teacher(t_id1) on update cascade on delete cascade,
    t_id2 raw references teacher(t_id2) on update cascade on delete cascade,
    s_name varchar not null
);
insert into teacher values (empty_blob(), HEXTORAW('DEADBEEF'), '王老师');
insert into student values (1, empty_blob(), HEXTORAW('DEADBEEF'), '李四');
select * from student;
update teacher set t_id2 = HEXTORAW('EEEEEFFF') where t_id2 = HEXTORAW('DEADBEEF');
select * from student;
delete from teacher where t_id1 = empty_blob();
select * from student;
drop table if exists student;
drop table if exists teacher;
--测试点5：日期/时间类型
drop table if exists student;
drop table if exists teacher;
create table teacher
(
    t_id1 date primary key,
    t_id2 time without time zone unique,
    t_id3 time with time zone unique,
    t_id4 timestamp without time zone unique,
    t_id5 timestamp with time zone unique,
    t_id6 smalldatetime unique,
    t_id7 INTERVAL DAY(3) TO SECOND (4) unique,
    t_id8 interval year(6) UNIQUE,
    t_id9 reltime UNIQUE,
    t_name varchar not null
);
create table student
(
    s_id int primary key,
    t_id1 date references teacher(t_id1) on update cascade on delete cascade,
    t_id2 time without time zone references teacher(t_id2) on update cascade on delete cascade,
    t_id3 time with time zone references teacher(t_id3) on update cascade on delete cascade,
    t_id4 timestamp without time zone references teacher(t_id4) on update cascade on delete cascade,
    t_id5 timestamp with time zone references teacher(t_id5) on update cascade on delete cascade,
    t_id6 smalldatetime references teacher(t_id6) on update cascade on delete cascade,
    t_id7 INTERVAL DAY(3) TO SECOND references teacher(t_id7) on update cascade on delete cascade,
    t_id8 interval year(6) references teacher(t_id8) on update cascade on delete cascade,
    t_id9 reltime references teacher(t_id9) on update cascade on delete cascade,
    s_name varchar not null
);
insert into teacher values ('12-10-2010', '21:21:21', '21:21:21 pst', '2010-12-12', '2013-12-11 pst', '2003-04-12 04:05:06', INTERVAL '3' DAY, interval '2' year, '90', '王老师');
insert into student values (1, '12-10-2010', '21:21:21', '21:21:21 pst', '2010-12-12', '2013-12-11 pst', '2003-04-12 04:05:06', INTERVAL '3' DAY, interval '2' year, '90', '李四');
select * from student;
update teacher set t_id9 = '60' where t_id9 = '90';
select * from student;
delete from teacher where t_id1 = '12-10-2010';
select * from student;
drop table if exists student;
drop table if exists teacher;
--测试点6：其他类型（货币类型、位串类型、网络地址类型）
drop table if exists student;
drop table if exists teacher;
create table teacher
(
    t_id1 money primary key,
    t_id2 bit(3) unique,
    t_id3 bit varying(5) unique,
    t_id4 cidr unique,
    t_id5 inet unique,
    t_id6 macaddr unique,
    t_name varchar not null
);
create table student
(
    s_id int primary key,
    t_id1 money references teacher(t_id1) on update cascade on delete cascade,
    t_id2 bit(3) references teacher(t_id2) on update cascade on delete cascade,
    t_id3 bit varying(5) references teacher(t_id3) on update cascade on delete cascade,
    t_id4 cidr references teacher(t_id4) on update cascade on delete cascade,
    t_id5 inet references teacher(t_id5) on update cascade on delete cascade,
    t_id6 macaddr references teacher(t_id6) on update cascade on delete cascade,
    s_name varchar not null
);
insert into teacher values (123.12,  B'101', B'00', '192.168.100.128/25', '192.168.31.32/24', '08:00:2b:01:02:03', '王老师');
insert into student values (1, 123.12,  B'101', B'00', '192.168.100.128/25', '192.168.31.32/24', '08:00:2b:01:02:03', '李四');
select count(*) from student;
update teacher set t_id2 = B'100' where t_id2 = B'101';
select count(*) from student;
delete from teacher where t_id4 = '192.168.100.128/25';
select * from student;
drop table if exists student;
drop table if exists teacher;
