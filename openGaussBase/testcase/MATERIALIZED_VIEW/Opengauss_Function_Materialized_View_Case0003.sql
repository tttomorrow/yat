-- @testpoint: 测试创建物化视图时指定查询语句，合理报错

--创建物化视图（指定查询语句）
drop table if exists student cascade;
create table student
(
    id int primary key,
    name varchar(10) not null
);
insert into student values (1, 'aaa');
insert into student values (2, 'bbb');
insert into student values (3, 'ccc');
insert into student values (4, 'ddd');
insert into student values (5, 'eee');
insert into student values (6, 'fff');
create materialized view student_mv1 as select * from student;
create materialized view student_mv2 as table student;
select * from student_mv1;
select * from student_mv2;
drop table student cascade;
--另一种用法
drop materialized view if exists student_mv;
create materialized view student_mv as values (1, 'aaa'), (2, 'bbb');
select * from student_mv;
drop materialized view student_mv;
--创建物化视图时查询语句出错
create materialized view student_mv1 as select 1/0 as x;--error
create materialized view student_mv2 as select 1/0 as x with no data;--尚未出错
select * from student_mv2;
refresh materialized view student_mv2;--error
drop materialized view student_mv2;
