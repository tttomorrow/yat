--  @testpoint:使用insert...update语句插入一条数据,主键列数据已存在，其他列数据不存在，name列值更新
--预置条件enable_upsert_to_merge为off
drop table if exists products7;
--建表指定一列是主键
CREATE TABLE products7 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规insert插入一条语句
insert into  products7 values(01,'grains',5.5);
select * from  products7;
--使用insert...update插入一条数据， update name列，name列值更新，原数据(01,'grains',5.5)更改为(01,'veggies',5.5)
insert into  products7 values(01,'veggies',6.8) on DUPLICATE key update name='veggies';
select * from  products7;
drop table products7;