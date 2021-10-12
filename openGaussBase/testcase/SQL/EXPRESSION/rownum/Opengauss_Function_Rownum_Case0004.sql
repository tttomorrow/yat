-- @testpoint: 测试rownum在联结中的情况

drop table if exists student_bk;
drop table if exists student;
create table student
(
    id int primary key,
    name varchar(10) not null,
    class int
);
create table student_bk
(
    id_bk int primary key,
    name_bk varchar(10) not null,
    class_bk int
);
--测试点1：left join
select rownum, * from student left join student_bk on class = class_bk;
select rownum, * from student left join student_bk on class = class_bk where rownum != 4;
--测试点2：right join
select rownum, * from student right join student_bk on class = class_bk;
select rownum, * from student right join student_bk on class = class_bk where rownum != 3;
--测试点3：inner join
select rownum, * from student inner join student_bk on class = class_bk;
select rownum, * from student inner join student_bk on class = class_bk where rownum != 3;
--测试点4：full join
select rownum, * from student full join student_bk on class = class_bk;
select rownum, * from student full join student_bk on class = class_bk where rownum != 5;
--测试点5：等值联结
select rownum, * from student, student_bk where student.class = student_bk.class_bk;
select rownum, * from student, student_bk where student.class = student_bk.class_bk and rownum != 2;
drop table if exists student_bk;
drop table if exists student;
