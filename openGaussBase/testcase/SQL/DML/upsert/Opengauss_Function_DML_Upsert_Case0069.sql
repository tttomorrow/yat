--  @testpoint:创建表指定其中一列是主键并定义数据类型是序列型,使用insert...update语句并添加关键字EXCLUDED
--预置条件enable_upsert_to_merge为off
drop table if exists course_01;
--建表，指定一列是主键
create table course_01 (id serial primary key,
name varchar(50)
);
--常规插入一条数据，id为1
insert into course_01 values(default,'maths');
select * from course_01;
--使用insert...update语句并添加关键字EXCLUDED，数据更改为(1,)
insert into course_01 values(1) ON DUPLICATE key update  name=EXCLUDED.name;
select * from course_01;
--使用insert...update语句并添加关键字EXCLUDED，id列插入2，name列为空
insert into course_01 values(default) ON DUPLICATE key update  name=EXCLUDED.name;
select * from course_01;
--使用insert...update语句并添加关键字EXCLUDED，修改字段id为2的name字段为'music'
insert into course_01 values(2,'music') ON DUPLICATE key  update name=EXCLUDED.name;
select * from course_01;
--使用insert...update语句并添加关键字EXCLUDED，新增一条数据(3,'piano')
insert into course_01 values(default,'piano') ON  DUPLICATE key update  name=EXCLUDED.name;
select * from course_01;
drop table course_01;