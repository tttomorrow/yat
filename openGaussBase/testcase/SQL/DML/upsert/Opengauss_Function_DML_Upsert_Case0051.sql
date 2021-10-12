--  @testpoint:创建表时未设置主键约束，使用insert...update语句并添加关键字EXCLUDED，正常插入数据
----预置条件enable_upsert_to_merge为off
drop table if exists products_b4;
--建表，指定一列是主键
CREATE TABLE products_b4 (
    product_no integer ,
    name text,
    price numeric
);


--使用insert...update语句插入一条数据，数据插入成功
insert into  products_b4 values(02,'grains',5.5) on DUPLICATE key update name=EXCLUDED.name, price=EXCLUDED.price;
select * from  products_b4;
drop table products_b4;