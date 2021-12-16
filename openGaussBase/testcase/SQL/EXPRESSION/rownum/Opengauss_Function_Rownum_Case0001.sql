-- @testpoint: 测试rownum支持别名，合理报错
--             规则：含有where的select语句，不能使用本层和外层的rownum别名

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
--测试点1：单层select中使用别名
select rownum rowno, * from student;
--测试点2：对上一个别名加入where的判断
select rownum rowno, * from student where rownum < 5;
select rownum rowno, * from student where rowno < 5;
--测试点3：多层select中使用别名，不在同一层使用
select rownum rowno2, * from (select rownum rowno1, * from student) where rowno1 < 3;
select rownum rowno2, * from (select rownum rowno1, * from student where rownum < 5) where rowno1 < 3;
--测试点4：多层select中使用别名，最外层在本层中使用
select rownum rowno2, * from (select rownum rowno1, * from student) where rowno2 < 2;
select rownum rowno2, * from (select rownum rowno1, * from student where rowno1 < 5) where rowno2 < 3;
select rownum rowno2, * from (select rownum rowno1, * from student where rowno2 < 5) where rowno1 < 3;

drop table if exists student;
