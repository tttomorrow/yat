--  @testpoint:使用insert...update语句插入一条数据，添加EXCLUDED关键字，主键列数据不存在，其他列数据已存在
--预置条件enable_upsert_to_merge为off
drop table if exists products28;
--建表，指定一列是主键
CREATE TABLE products28 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规插入一条数据
insert into  products28 values(10,'grains',5.5);
select * from  products28;
--添加EXCLUDED关键字,update product_no 列，合理报错
insert into  products28 values(11,'grains',5.5) on DUPLICATE key update  product_no =EXCLUDED.product_no;
select * from  products28;
drop table products28;