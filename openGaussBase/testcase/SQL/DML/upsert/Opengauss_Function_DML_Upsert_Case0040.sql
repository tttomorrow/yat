--  @testpoint:使用insert...update插入两条数据,添加关键字EXCLUDED，第一条数据主键列数据不存在，其他列数据已存在;第二条数据主键列数据不存在，其他列数据已存在
--预置条件enable_upsert_to_merge为off
drop table if exists upsert_b1;
create table upsert_b1(id int primary key,age int,count int);
--建表，指定一列是主键
--常规插入一条数据
insert into upsert_b1 values (1,1,1),(4,4,4);
select * from upsert_b1;
--update主键列id为EXCLUDED.id，合理报错
insert into upsert_b1 values(2,1,4),(3,3,5) ON DUPLICATE key update id=EXCLUDED.id;
--update age为EXCLUDED.age，新插入两条数据(2,1,4),(3,3,5)
insert into upsert_b1 values(2,1,4),(3,3,5) ON DUPLICATE key update age=EXCLUDED.age;
select * from upsert_b1;
delete from upsert_b1;
insert into upsert_b1 values (1,1,1),(4,4,4);
--update age为EXCLUDED.age，count为EXCLUDED.count,新插入两条数据(2,1,4),(3,3,5)
insert into upsert_b1 values(2,1,4),(3,3,5) ON DUPLICATE key update  age=EXCLUDED.age,count=EXCLUDED.count;
select * from upsert_b1;
drop table upsert_b1;