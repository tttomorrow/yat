--  @testpoint:使用insert...update插入两条数据,第一条数据主键列数据已存在，其他列数据不存在;第二条数据主键列数据已存在，其他列数据不存在
--预置条件enable_upsert_to_merge为off
drop table if exists upsert1;
--建表，指定一列是主键
create table upsert1(id int primary key,age int,count int);
insert into upsert1 values (1,1,1),(4,4,4);
select * from upsert1;

--update id列为1,合理报错
insert into  upsert1 values(1,2,3),(4,5,6) on DUPLICATE key update id=1;
--update id列为4,合理报错
insert into  upsert1 values(1,2,3),(4,5,6) on DUPLICATE key update id=4;

--update age为2，数据(1,1,1)和(4,4,4)更改为(1,2,1)和(4,2,4)
insert into upsert1 values(1,2,3),(4,5,6) ON DUPLICATE key update age=2;
select * from upsert1;
delete from upsert1;
insert into upsert1 values (1,1,1),(4,4,4);

--update age列为5，数据(1,1,1)和(4,4,4)更改为(1,5,1)和(4,5,4)
insert into upsert1 values(1,2,3),(4,5,6) ON DUPLICATE key update  age=5;
select * from upsert1;
delete from upsert1;
insert into upsert1 values (1,1,1),(4,4,4);

 --update age为2，count为3，数据(1,1,1),(4,4,4)更改为(1,2,3)和(4,2,3)
 insert into upsert1 values(1,2,3),(4,5,6) ON DUPLICATE key update  age=2,count=3;
 select * from upsert1;
 delete from upsert1;
 insert into upsert1 values (1,1,1),(4,4,4);

 --update age为5，count为6，数据(1,1,1),(4,4,4)更改为(1,5,6)和(4,5,6)
  insert into upsert1 values(1,2,3),(4,5,6) ON DUPLICATE key update  age=5,count=6;
  select * from upsert1;
  drop table upsert1;