--  @testpoint:使用insert...update插入两条数据,第一条数据主数据主键列数据不存在，其他列数据已存在;第二条数据主键列数据不存在，其他列数据已存在
----预置条件enable_upsert_to_merge为off
drop table if exists upsert1;
--建表，指定一列是主键
create table upsert1(id int primary key,age int,count int);
insert into upsert1 values (1,1,1),(4,4,4);
select * from upsert1;

--update主键列id为2，合理报错
insert into upsert1 values(2,1,1),(3,4,4) ON DUPLICATE key update id=2;
--update主键列id为3，合理报错
insert into upsert1 values(2,1,1),(3,4,4) ON DUPLICATE key update id=3;

--主键不重复，update age为1，新插入两条数据(2,1,1),(3,4,4)
insert into upsert1 values(2,1,1),(3,4,4) ON DUPLICATE key update age=1;
select * from upsert1;
delete from upsert1 ;
insert into upsert1 values (1,1,1),(4,4,4);

--主键不重复，update age列为4，新插入两条数据(2,1,1),(3,4,4)
insert into upsert1 values(2,1,1),(3,4,4) ON DUPLICATE key update age=4;
select * from upsert1;
drop table upsert1;