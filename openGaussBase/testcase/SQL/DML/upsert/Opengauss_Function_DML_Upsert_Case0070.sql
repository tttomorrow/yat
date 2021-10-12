--  @testpoint:创建表指定其中一列是主键并定义数据类型是序列型,使用insert...nothing语句
--预置条件enable_upsert_to_merge为off
drop table if exists course_02;
--建表，指定一列是主键
create table course_02 (id serial primary key,
name varchar(50)
);
--常规插入一条数据，id为1
insert into course_02 values(default,'maths');
select * from course_02;

--使用insert...nothing语句，主键列1已存在,直接返回
insert into course_02 values(1,'Chinese') ON  DUPLICATE key update nothing ;
select * from course_02;

--使用insert...nothing语句,主键列不存在，新增一条数据(2,'dance')
insert into course_02 values(default,'dance') ON  DUPLICATE key update nothing ;
select * from course_02;

--使用insert...nothing语句,主键列不插入值，新增一条数据(3,guitar)
insert into course_02(name) values('guitar') ON DUPLICATE key update nothing;
select * from course_02;
--使用insert...nothing语句,主键列插入null值，合理报错
insert into course_02 values(null,'guitar') ON DUPLICATE key update nothing;
select * from course_02;
drop table course_02;