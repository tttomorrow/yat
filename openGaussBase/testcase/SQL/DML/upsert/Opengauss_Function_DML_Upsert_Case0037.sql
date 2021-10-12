--  @testpoint:使用insert...update插入两条数据,添加EXCLUDED关键字,第一条数据主键列数据已存在，其他列数据不存在;第二条数据主键列数据已存在，其他列数据不存在
--预置条件enable_upsert_to_merge为off
drop table if exists upsert10;
--建表，指定一列是主键
create table upsert10(id int primary key,age int,count int);
insert into upsert10 values (1,1,1),(4,4,4);
select * from upsert10;
--update id列为EXCLUDED.id,合理报错
insert into  upsert10 values(1,2,3),(4,5,6) on DUPLICATE key update id=EXCLUDED.id;
--update age列为EXCLUDED.age，(1,1,1)数据改为(1,2,1);(4,4,4)数据改为(4,5,4);
insert into upsert10 values(1,2,3),(4,5,6) ON DUPLICATE key update age=EXCLUDED.age;
select * from upsert10;
delete from upsert10;
insert into upsert10 values (1,1,1),(4,4,4);
 --update age为EXCLUDED.age，count为EXCLUDED.count，数据(1,1,1)更改为(1,2,3)，(4,4,4)更改为(4,5,6)
 insert into upsert10 values(1,2,3),(4,5,6) ON DUPLICATE key update  age=EXCLUDED.age,count=EXCLUDED.count;
select * from upsert10;
drop table upsert10;

