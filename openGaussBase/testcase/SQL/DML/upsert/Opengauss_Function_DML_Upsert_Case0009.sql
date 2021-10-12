--  @testpoint:使用insert...update语句插入一条数据,主键列数据不存在，其他列数据不存在，新插入一条数据
--预置条件enable_upsert_to_merge为off
drop table if exists products6;
--建表指定一列是主键
CREATE TABLE products6 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规insert插入一条数据
insert into  products6 values(01,'grains',5.5);
select * from  products6;
--使用insert...update插入一条数据，update  name ，price列，新增一条数据(02,'veggies',6.8)
insert into  products6 values(02,'veggies',6.8) on DUPLICATE key update name='veggies',price=6.8;
select * from  products6;
drop table products6;