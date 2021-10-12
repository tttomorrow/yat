--  @testpoint:使用insert...update语句插入一条数据，添加EXCLUDED关键字，主键列数据已存在，其他列数据不存在
--预置条件enable_upsert_to_merge为off
drop table if exists products22;
--建表，指定一列是主键
CREATE TABLE products22 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规插入一条数据
insert into  products22 values(10,'grains',5.5);
select * from products22;
--使用insert...update语句插入一条数据，添加EXCLUDED关键字,update主键 product_no列，合理报错
insert into  products22 values(10,'meat',22.8) on DUPLICATE key update product_no=EXCLUDED.product_no ;
select * from  products22;
drop table products22;