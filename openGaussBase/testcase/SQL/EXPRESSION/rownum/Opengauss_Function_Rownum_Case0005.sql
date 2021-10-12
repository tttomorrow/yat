-- @testpoint: 测试rownum在DDL中的表现

drop table if exists student;
create table student
(
    s_id int primary key,
    s_name varchar(10) not null
);
--测试点1：insert
insert into student values ((select s_id from student where rownum <= 1) + 6, 'ggg');
select * from student;
--测试点2：delete
delete from student where rownum != 3;
select * from student;
--测试点3：update
update student set s_name = 'nnn' where rownum != 3;
select * from student;
--测试点4：select
--已在其它用例中覆盖

