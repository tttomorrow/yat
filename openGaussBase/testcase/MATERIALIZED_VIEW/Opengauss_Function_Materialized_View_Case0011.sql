-- @testpoint: 测试物化视图对临时表的支持情况，合理报错

--临时表支持情况，临时表不支持
--会话级本地临时表
create temporary table student_t
(
    id int primary key,
    name varchar(10) not null
) on commit preserve rows;
insert into student_t values (1, 'aaa');
create materialized view student_t_mv as select * from student_t;
drop table student_t cascade;
--事务级本地临时表
start transaction;
create temporary table student_t
(
    id int primary key,
    name varchar(10) not null
) on commit delete rows;
insert into student_t values (1, 'aaa');
create materialized view student_t_mv as select * from student_t;
commit;
drop table student_t cascade;
--会话级全局临时表
create global temporary table student_gt
(
    id int primary key,
    name varchar(10) not null
) on commit preserve rows;
insert into student_gt values (1, 'aaa');
create materialized view student_t_mv as select * from student_gt;
drop table student_gt cascade;
--事务级全局临时表
start transaction;
create global temporary table student_gt
(
    id int primary key,
    name varchar(10) not null
) on commit delete rows;
insert into student_gt values (1, 'aaa');
create materialized view student_t_mv as select * from student_gt;
commit;
drop table student_gt cascade;
