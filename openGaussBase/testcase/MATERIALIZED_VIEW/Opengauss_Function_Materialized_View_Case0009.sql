-- @testpoint: 测试在物化视图中执行DDL（select），合理报错

--物化视图执行DDL（select）
drop table if exists student cascade;
drop table if exists class cascade;
create table class
(
    class_id int primary key,
    class_name varchar(10) not null
);
create table student
(
    id int primary key,
    name varchar(10) not null,
    class_id int
);
insert into class values (101, '1-1');
insert into class values (102, '1-2');
insert into class values (104, '1-4');
insert into student values (1, 'aaa', 101);
insert into student values (2, 'bbb', 101);
insert into student values (3, 'ccc', 102);
insert into student values (4, 'ddd', 102);
insert into student values (5, 'eee', 102);
insert into student values (6, 'fff', 103);
--子查询 && 子链接 && 组合查询 && order by
create materialized view student_mv as select * from student where class_id in (select class_id from class);
select * from student_mv;
select * from student_mv where class_id = 101;
select * from class where class_id in (select class_id from student_mv);
--组合查询1
create materialized view student_mvv as select id, name from student_mv union select class_id, class_name from class;--union
select * from student_mvv where id < 103 order by id desc;
--别名检查
select id nid, name noname from student_mvv;
--增加/删除被参照表列
alter table class drop column class_id;--error
refresh materialized view student_mvv;
alter table class add column id_new int;
refresh materialized view student_mvv;--未报错，与pg保持一致
select * from student_mvv;
--修改被参照表列名
alter table class rename column class_id to class_id_new;
refresh materialized view student_mvv;--ok
select * from student_mvv;
--组合查询2
create view student_mv_v as select * from student_mv;
create materialized view student_mv_mvv as select * from student_mv_v minus select * from student_mv;--minus
insert into student values (7, 'ggg', 104);
refresh materialized view student_mv;
refresh materialized view student_mv_mvv;
select * from student_mv_mvv;
--查看执行计划
EXPLAIN (analyze on, costs off) 
select * from student_mv where class_id = 101;
--清理环境
drop table if exists student cascade;
drop table if exists class cascade;