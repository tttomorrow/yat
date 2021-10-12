-- @testpoint: 测试创建物化视图时指定指定表空间名

drop table if exists student cascade;
drop tablespace if exists mv_space;
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
create tablespace mv_space relative location 'postgres_tbs';
create materialized view student_mv tablespace mv_space as select * from student;
select spcname from pg_tablespace where oid = (select reltablespace from pg_class where relname = 'student_mv');
drop table student cascade;
drop tablespace mv_space;