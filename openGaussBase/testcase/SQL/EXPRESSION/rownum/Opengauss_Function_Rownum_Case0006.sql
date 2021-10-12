-- @testpoint: 测试rownum在子查询/子链接中的表现

drop table if exists student;
create table student
(
    s_id int primary key,
    s_name varchar(10) not null
);
--测试点1：两层子链接
select * from student where s_id in (select s_id from student where rownum < 3 union select s_id from student where rownum != 5);
--测试点2：三层子查询/子链接混用
select * from student where s_id in (select s_id from student where rownum < 3 union select * from (select s_id from student order by 1 desc) as result where rownum != 5);
drop table if exists student;
