-- @testpoint: 一些发散性测试，合理报错

--发散测试
--唯一性索引约束
drop materialized view if exists student_mv;
create materialized view student_mv(id, name) as values (1, 'aaa'), (1, 'bbb');
select * from student_mv;
create unique index index_test on student_mv(id);--error
select * from student_mv;
drop materialized view student_mv;
--建立索引后更新数据
drop table if exists student cascade;
create table student
(
    id int,
    name varchar(10) not null
);
insert into student values (1, 'aaa');
insert into student values (2, 'bbb');
insert into student values (3, 'ccc');
create materialized view student_mv(id, name) as select * from student;
create unique index index_test on student_mv(id);
insert into student values (1, 'aaa');
refresh materialized view student_mv;--error
--外键约束
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
create table foreign_key_table
(
    id int primary key,
    s_id int references student_mv(id) on update cascade on delete no action
);--error
--事务回滚
insert into student values (7, 'ggg');
select * from student_mv;--6
start transaction;
refresh materialized view student_mv;
select * from student_mv;--7
abort;
select * from student_mv;--6
--vacuum
delete from student where id > 4;
vacuum;
select * from student_mv;
drop table student cascade;
