-- @testpoint: 测试rownum在group by中的表现，合理报错

drop table if exists student;
create table student
(
    id int primary key,
    class int,
    name varchar(10) not null
);
insert into student values (2017100001, 1, 'aaa');
insert into student values (2017100002, 1, 'bbb');
insert into student values (2017100003, 1, 'ccc');
insert into student values (2017100004, 2, 'ddd');
insert into student values (2017100005, 2, 'eee');
insert into student values (2017100006, 2, 'fff');
insert into student values (2017100007, 2, 'ggg');
insert into student values (2017100008, 3, 'hhh');
insert into student values (2017100009, 3, 'iii');
insert into student values (2017100010, 4, 'jjj');
--分别测试rownum在where和having中的作用
select count(id), class from student where rownum < 6 group by class;
select count(id), class from student group by class having rownum < 4;
select count(id), count(class) from student group by rownum having rownum < 4;
--ok，在where和having中都出现，各代表了不同的含义
select count(id), class from student where rownum != 9 group by class having class < 4;
drop table if exists student;
