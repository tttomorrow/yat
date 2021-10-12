--  @testpoint:使用insert...update插入两条数据,添加关键字EXCLUDED，第一条数据主数据主键列数据已存在，其他列数据不存在;第二条数据主键列数据不存在，其他列数据不存在
--预置条件enable_upsert_to_merge为off
drop table if exists upsert_a2;
--建表，指定一列是主键
create table upsert_a2(id int primary key,age int,count int);
--常规插入一条数据
insert into upsert_a2 values (1,1,1),(4,4,4);
select * from upsert_a2;
--update主键列id为EXCLUDED.id，合理报错
insert into upsert_a2 values(1,2,3),(2,3,4) ON DUPLICATE key update id=EXCLUDED.id;

--update age为EXCLUDED.age，修改(1,1,1)为(1,2,1)并且插入一条新数据(2,3,4)
insert into upsert_a2 values(1,2,3),(2,3,4) ON DUPLICATE key update age=EXCLUDED.age;
select * from upsert_a2;
delete from upsert_a2 ;
insert into upsert_a2 values (1,1,1),(4,4,4);
 --update age为EXCLUDED.age,count为EXCLUDED.count,修改(1,1,1)这条数据的为(1,2,3)并且插入一条新数据(2,3,4)
 insert into upsert_a2 values(1,2,3),(2,3,4) ON DUPLICATE key update age=EXCLUDED.age,count=EXCLUDED.count;
 select * from upsert_a2;
 drop table upsert_a2;
