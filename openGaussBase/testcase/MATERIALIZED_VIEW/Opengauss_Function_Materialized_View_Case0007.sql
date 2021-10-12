-- @testpoint: 测试删除物化视图，合理报错

--删除物化视图
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
create view student_mv_v (id, name) as select * from student_mv;
--删除物化视图，默认
drop materialized view student_mv;--error
--删除物化视图，restrict
drop materialized view student_mv restrict;--error
--删除物化视图，cascade
drop materialized view student_mv cascade;
select * from student_mv_v;--error
