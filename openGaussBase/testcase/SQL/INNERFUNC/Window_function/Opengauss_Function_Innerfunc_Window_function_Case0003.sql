-- @testpoint: RANK() 描述：为各组内值生成跳跃排序序号，其中，相同的值具有相同序号

create table course_table ( id int, grade varchar ( 10 ), course varchar ( 10 ) );
insert into course_table values
(1,'一年级','心理学'),
(2,'二年级','社会学'),
(3,'三年级','社会学'),
(4,'一年级','刑侦学'),
(5,'二年级','心理学'),
(6,'三年级','计算机'),
(7,'一年级','刑侦学'),
(8,'二年级','心理学'),
(9,'三年级','社会学'),
(10,'一年级','社会学'),
(11,'二年级','社会学'),
(12,'二年级','计算机'),
(13,'一年级','心理学'),
(14,'三年级','刑侦学'),
(15,'三年级','计算机');

--查看表结构
select * from course_table;

--使用rank()函数，为各组内值生成跳跃排序序号，其中，相同的值具有相同序号
select id, course, rank ( ) over ( partition by grade order by course desc ) from course_table;

--清理环境
drop table course_table;