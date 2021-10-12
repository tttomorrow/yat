--  @testpoint:使用insert...update语句插入一条数据，添加EXCLUDED关键字，主键列数据已存在，其他列数据不存在
--预置条件enable_upsert_to_merge为off
drop table if exists products23;
--建表，指定一列是主键
CREATE TABLE products23 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规插入一条数据
insert into  products23 values(10,'grains',5.5);
select * from  products23;
--添加EXCLUDED关键字,主键列重复，update name列，name列的值改为'meat'
insert into  products23 values(10,'meat',22.8) on DUPLICATE key update name=EXCLUDED.name ;
select * from  products23;
drop table products23;