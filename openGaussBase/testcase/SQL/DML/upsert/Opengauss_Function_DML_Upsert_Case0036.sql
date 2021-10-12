--  @testpoint:使用insert...update语句插入一条数据，添加EXCLUDED关键字，主键列数据不存在，其他列数据不存在，新插入一条数据成功
--预置条件enable_upsert_to_merge为off
drop table if exists products33;
--建表，指定一列是主键
CREATE TABLE products33 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规插入一条数据
insert into  products33 values(10,'grains',5.5);
select * from  products33;
--使用insert...update语句插入一条数据，添加EXCLUDED关键字,update name列和price列，新插入一条数据成功
insert into  products33 values(11,'apple',5.9) on DUPLICATE key update name=EXCLUDED.name,price=EXCLUDED.price;
select * from  products33;
drop table products33;


