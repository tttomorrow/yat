--  @testpoint:使用insert...update插入两条数据,第一条数据主数据主键列数据已存在，其他列数据不存在;第二条数据主键列数据不存在，其他列数据不存在
----预置条件enable_upsert_to_merge为off
drop table if exists upsert1;
--建表，指定一列是主键
create table upsert1(id int primary key,age int,count int);
insert into upsert1 values (1,1,1),(4,4,4);
select * from upsert1;

--update age为2，count为3，修改(1,1,1)这条数据为(1,2,3)并且新插入一条数据(2,3,4)
insert into upsert1 values(1,2,3),(2,3,4) ON DUPLICATE key update age=2,count=3;
select * from upsert1;
delete from upsert1 ;
insert into upsert1 values (1,1,1),(4,4,4);

--update age为3，count为4，修改(1,1,1)这条数据为(1,3,4)并且新插入一条数据(2,3,4)
insert into upsert1 values(1,2,3),(2,3,4) on DUPLICATE key update age=3,count=4;
select * from upsert1;
drop table upsert1;