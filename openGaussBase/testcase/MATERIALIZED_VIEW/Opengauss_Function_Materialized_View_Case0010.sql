-- @testpoint: 测试物化视图对列存表的支持情况

--列存表支持情况
drop table if exists student cascade;
create table student
(
    id int,
    name varchar(10) not null
) with (orientation = column);
insert into student values (1, 'aaa');
insert into student values (2, 'bbb');
insert into student values (3, 'ccc');
insert into student values (4, 'ddd');
insert into student values (5, 'eee');
insert into student values (6, 'fff');
create materialized view student_mv as select * from student;
drop table student cascade;
