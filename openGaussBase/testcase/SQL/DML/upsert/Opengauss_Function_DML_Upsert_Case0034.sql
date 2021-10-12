--  @testpoint:使用insert...update语句插入一条数据，添加EXCLUDED关键字，主键列数据不存在，其他列数据不存在
--预置条件enable_upsert_to_merge为off
drop table if exists products31;
----建表，指定一列是主键
CREATE TABLE products31 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规插入一条数据
insert into  products31 values(10,'grains',5.5);
select * from  products31;
--添加EXCLUDED关键字,主键列不重复，update  product_no 列，合理报错
insert into  products31 values(11,'apple',6.2) on DUPLICATE key update product_no=EXCLUDED.product_no;
select * from  products31;
drop table products31;