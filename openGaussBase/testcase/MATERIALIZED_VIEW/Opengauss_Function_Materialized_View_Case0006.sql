-- @testpoint: 测试更新物化视图，合理报错

--更新物化视图
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
create materialized view student_mv (id, name) as select * from student;
select * from student_mv;
--物化视图结果不会实时更新
insert into student values (7, 'ggg');
select * from student_mv;
--更新物化视图结果，默认
refresh materialized view student_mv;
select * from student_mv;
--更新物化视图结果，with no data
refresh materialized view student_mv with no data;
select * from student_mv;
--更新物化视图结果，with data
refresh materialized view student_mv with data;
select * from student_mv;
--更新物化视图，增量刷新
insert into student values (8, 'hhh');
insert into student values (9, 'iii');
refresh materialized view concurrently student_mv;--error
select relispopulated from pg_class where relname = 'student_mv';--error
--查看执行计划
create or replace procedure mv_proc(loopnum in integer)
is
insertid integer;
startid integer;
begin
select max(id) from student into startid;
for i in 1..loopnum
loop
insertid := i+startid;
insert into student values (insertid, 'ooo');
end loop;
end;
/
call mv_proc(10000);
explain (analyze on, costs off) refresh materialized view student_mv;
