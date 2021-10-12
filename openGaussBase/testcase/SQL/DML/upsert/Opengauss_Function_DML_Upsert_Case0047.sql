--  @testpoint:使用insert...update插入两条数据,第一条数据主数据主键列数据不存在，其他列数据已存在;第二条数据主键列数据不存在，其他列数据已存在
----预置条件enable_upsert_to_merge为off
drop table if exists upsert2;
--建表，指定一列是主键
create table upsert2(id int primary key,age int,count int);
insert into upsert2 values (1,1,1),(4,4,4);
select * from upsert2;

--主键不重复，upadte age为1，count为1，新插入两条数据
insert into upsert2 values(2,1,1),(3,4,4) ON DUPLICATE key update age=1,count=1;
select * from upsert2;
delete from upsert2;
insert into upsert2 values (1,1,1),(4,4,4);

--主键不重复，upadte age为4，count为4，新插入两条数据
insert into upsert2 values(2,1,1),(3,4,4) ON DUPLICATE key update age=4,count=4;
select * from upsert2;
drop table upsert2;