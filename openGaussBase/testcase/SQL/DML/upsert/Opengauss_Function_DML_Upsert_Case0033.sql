--  @testpoint:使用insert...update语句插入一条数据，添加EXCLUDED关键字，主键列数据不存在，其他列数据已存在，新插入一条数据成功
--预置条件enable_upsert_to_merge为off
drop table if exists products30;
--建表，指定一列是主键
CREATE TABLE products30 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规插入一条数据
insert into  products30 values(10,'grains',5.5);
select * from  products30;
--使用insert...update语句插入一条数据，添加EXCLUDED关键字,update name列和price列，新插入一条数据成功
insert into  products30 values(11,'apple',5.6) on DUPLICATE key update name =EXCLUDED.name,price=EXCLUDED.price;
select * from  products30;
drop table products30;