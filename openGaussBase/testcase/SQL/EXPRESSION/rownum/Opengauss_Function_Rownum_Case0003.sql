-- @testpoint: 测试rownum在组合查询中的表现

drop table if exists student;
drop table if exists teacher;
create table student
(
    s_id int primary key,
    s_name varchar(10) not null
);
create table teacher
(
    t_id int primary key,
    t_name varchar(10) not null
);
--测试点1：union
--简单的情况，包含子查询和union all，重复信息能得以保留
select rownum, * from (select * from student union all select * from teacher) as result where rownum < 8;
--复杂一点了，子查询中包含了对rownum的限定，并且对union后的结果进行了rownum的限定
select rownum, * from (select * from student where rownum < 3 union select * from teacher where rownum != 4 order by 1 asc) as result where rownum != 3;
--再看下子查询中指定了别名，且union后的结果通过别名重新过滤，并对最终结果的rownum进行限定
select rownum, * from (select rownum rowno, * from student union all select rownum rowno, * from teacher) as result where (rowno < 3 or rowno != 5) and rownum < 9;
--测试点2：intersect
--简单的测试下子查询中包含intersect all
select rownum, * from (select * from student intersect all select * from teacher) as result where rownum <= 2;
--测试下包含了子查询rownum限定、排序，最终结果rownum限定的情况，和上面类似
select rownum, * from (select * from student where rownum != 6 intersect select * from teacher where rownum <= 3) as result where rownum != 2;
select rownum, * from (select * from student where rownum != 6 intersect select * from teacher where rownum <= 4 order by 1 asc) as result where rownum != 2;
--测试点3：except
--简单测试下except的基本功能
select rownum, * from (select * from student where rownum != 7 except select * from student where rownum <= 2) as result where rownum <= 3;
--测试下子查询结果排序，最终结果根据rownum再排序
select rownum, * from (select * from student where rownum <= 3 except select * from student where rownum != 2 order by 1 asc) as result order by 1 desc;
--测试点4：minus
--简单测试下minus基本功能（minus和except功能是一致的）
select rownum, * from (select rownum rowno, * from student where rownum != 7 minus select rownum rowno, * from student where rownum <= 3) where rowno >= 5;
--继续组合，测试下两层minus后的结果
select rownum, * from (select * from student minus select * from (select * from student where rownum != 7 minus select * from student where rownum <= 2) where rownum <= 2) order by 2 desc;
--针对上一个SQL颠倒下相减的顺序
select rownum, * from (select * from (select * from student where rownum != 7 minus select * from student where rownum <= 2) where rownum <= 2 minus select * from student) order by 1 desc;

drop table if exists student;
drop table if exists teacher;
