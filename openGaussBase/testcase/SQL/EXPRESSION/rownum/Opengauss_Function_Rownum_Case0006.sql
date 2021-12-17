-- @testpoint: 测试rownum在子查询/子链接中的表现

drop table if exists student;
create table student
(
    s_id int primary key,
    s_name varchar(10) not null
);
insert into student values (2017100001, 'aaa');
insert into student values (2017100002, 'bbb');
insert into student values (2017100003, 'ccc');
insert into student values (2017100004, 'ddd');
insert into student values (2017100005, 'eee');
insert into student values (2017100006, 'fff');
--测试点1：两层子链接
select * from student where s_id in (select s_id from student where rownum < 3 union select s_id from student where rownum != 5);
--测试点2：三层子查询/子链接混用
select * from student where s_id in (select s_id from student where rownum < 3 union select * from (select s_id from student order by 1 desc) as result where rownum != 5);
drop table if exists student;
