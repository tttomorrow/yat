-- @testpoint: 测试创建物化视图时指定指定表空间名

--创建物化视图（多级嵌套的物化视图）
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
create materialized view student_mv as select * from student;
select * from student_mv;
create materialized view student_mv_mv as select * from student_mv;
select * from student_mv_mv;
create view student_mv_mv_v as table student_mv_mv;
select * from student_mv_mv_v;
--查看执行计划
EXPLAIN (analyze on, costs off)
create materialized view student_mv_mv_v_mv as select * from student_mv_mv_v with no data;
select * from student_mv_mv_v_mv;
--插入一些数据，更新一下结果
insert into student values (7, 'ggg');
update student set id = 11 where name = 'aaa';
delete from student where id = 2;
select * from student;--yes
refresh materialized view student_mv_mv_v_mv;
select * from student_mv;--no
select * from student_mv_mv;--no
refresh materialized view student_mv;
refresh materialized view student_mv_mv;
select * from student_mv_mv;--yes
select * from student_mv_mv_v;--yes
select * from student_mv_mv_v_mv;--no
refresh materialized view student_mv_mv_v_mv;
select * from student_mv_mv_v_mv;--yes
drop table student cascade;
