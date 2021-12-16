-- @testpoint: 测试rownum在where条件中不同运算符下的表现，合理报错

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
insert into student values (2017100007, 'ggg');
insert into student values (2017100008, 'hhh');
insert into student values (2017100009, 'iii');
insert into student values (2017100010, 'jjj');
insert into student values (2017100011, 'kkk');
insert into student values (2017100012, 'lll');
--测试点1：rownum在 < 下的表现
select * from student where rownum < 1;
select * from student where rownum < 10;
--测试点2：rownum在 <= 下的表现
select * from student where rownum <= 1;
select * from student where rownum <= 20;
--测试点3：rownum在 = 下的表现
select * from student where rownum = 1;
select * from student where rownum = 5;
--测试点4：rownum在 != 下的表现
select * from student where rownum != 1;
select * from student where rownum != 7;
--测试点5：rownum在 > 下的表现
select * from student where rownum > 0;
select * from student where rownum > 5;
--测试点6：rownum在 >= 下的表现
select * from student where rownum >= 1;
select * from student where rownum >= 4;
--测试点7：rownum在between ... and ...下的表现
select * from student where rownum between 1 and 5;
select * from student where rownum between 3 and 12;
--测试点8：rownum在 < 和 <= 和 != 下组合使用
select * from student where rownum < 8 and rownum <= 6 and rownum != 7;
select * from student where rownum != 5 or rownum < 8;
select * from student where rownum <= 9 and rownum != 5 or rownum < 7;
--测试点9：rownum在表达式中包含运算表达式
select * from student where rownum < 7 + 9 - 13;
select * from student where rownum <= 2 * 3 - 2 / 2 + -3;
select to_hex(rownum + 1) from sys_dummy;
select mod(8, rownum * 3) from sys_dummy;
--测试点10：rownum与长整形、小数、负数比较
select * from student where rownum <= -3;
select * from student where rownum > -2;
select * from student where rownum != -5;
select * from student where rownum < 5.2;
select * from student where rownum != 7.23333333;
select * from student where rownum < 9223372036854775806;
select * from student where rownum < 2147483646;
select * from student where rownum < 32766;
--测试点11：rownum与其它数据类型比较
select * from student where rownum < false;
select * from student where rownum < true;
select * from student where rownum < 'a';
select * from student where rownum < HEXTORAW('EEEEEFFF');
select * from student where rownum < '12-10-2010';
--测试点12：rownum和变量比较
declare
tempNum int := 3;
begin
update student set s_name = 'zzz' where rownum < tempNum;
end;
/
select rownum, * from student;
drop table if exists student;
