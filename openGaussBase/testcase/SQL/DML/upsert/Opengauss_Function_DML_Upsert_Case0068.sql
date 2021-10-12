--  @testpoint:创建表指定其中一列是主键并定义数据类型是序列型,使用insert...update语句
--预置条件enable_upsert_to_merge为off
drop table if exists course;
--建表，指定一列是主键
create table course (id serial primary key,
name varchar(50)
);
--常规插入一条数据，id为1
insert into course values(default,'maths');
select * from course;
--使用insert..update插入一条数据，主键重复，原有数据(1,'maths')修改为(1,'English')
insert into course values(1) ON DUPLICATE key update  name='English';
select * from course;
--使用insert..update插入一条数据,主键不重复，新增一条数据(2,'Chinese')
insert into course values(default,'Chinese') ON DUPLICATE key update  name='Chinese';
select * from course;
drop table course;