-- @testpoint: 测试创建物化视图时指定列名，合理报错

--创建物化视图
--测试点1：测试创建物化视图时指定列名，基础功能
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
--不指定列名
create materialized view student_mv as select * from student;
select * from student_mv;
drop materialized view student_mv;
--指定列名，与被参照表相同
create materialized view student_mv (id, name) as select * from student;
select * from student_mv;
drop materialized view student_mv;
create materialized view student_mv (id, name) as select id, name from student;
select * from student_mv;
drop materialized view student_mv;
create materialized view student_mv (s_id, s_name) as select id s_id, name s_name from student;
select * from student_mv;
drop materialized view student_mv;
--指定列名，与被参照表不同
create materialized view student_mv (name, id) as select * from student;
select * from student_mv;
drop materialized view student_mv;
create materialized view student_mv (name, id) as select id s_id, name s_name from student;
select * from student_mv;
drop materialized view student_mv;
create materialized view student_mv (s_name, name) as select id s_id, name s_name from student;
select * from student_mv;
drop materialized view student_mv;
--测试点2：测试创建物化视图时指定列名，包含聚集函数
drop table if exists student cascade;
create table student
(
    id int primary key,
    name varchar(10) not null,
    score int,
    class_id int
);
insert into student values (1, 'aaa', 88, 101);
insert into student values (2, 'bbb', 70, 101);
insert into student values (3, 'ccc', 99, 102);
insert into student values (4, 'ddd', 45, 102);
insert into student values (5, 'eee', 98, 102);
insert into student values (6, 'fff', 90, 103);
--不指定列名
create materialized view student_mv as select count(score > 75), avg(score), max(score), min(score), class_id from student group by class_id;
select * from student_mv;
drop materialized view student_mv;
--指定列名
create materialized view student_mv (cont, avg, max, min, class_no) as select count(score > 75), avg(score), max(score), min(score), class_id from student group by class_id;
select * from student_mv;
drop materialized view student_mv;
--查看执行计划
EXPLAIN (analyze on, costs off) 
create materialized view student_mv (cont, avg, max, min, class_no) as select count(score > 75), avg(score), max(score), min(score), class_id from student group by class_id;
drop materialized view student_mv;
--物化视图中列数量与select中不符
create materialized view student_mv (name1, name2) as select count(score > 75), min(score), class_id from student group by class_id;
select * from student_mv;
drop materialized view student_mv;
--以下执行期望报错
create materialized view student_mv (name0, name0, name0, name0, name0, name0) as select count(score > 75), avg(score), max(score), min(score), class_id from student group by class_id;
create materialized view student_mv (name1, name2, name3, name4, name5) as select count(score > 75), min(score), class_id from student group by class_id;
drop table student;