-- @testpoint: 测试在物化视图中执行DDL（insert、update、delete），合理报错

--物化视图执行DDL（insert、update、delete）
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
--insert
insert into student_mv values (7. 'ggg');--error
--update
update student_mv set name = 'fff_new' where id = 1;--error
--delete
delete from student_mv where id = 1;--error
drop table student cascade;
