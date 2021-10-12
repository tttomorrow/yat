--  @testpoint:使用insert...update语句插入一条数据,主键列数据不存在，其他列数据不存在，update主键列，报错
----预置条件enable_upsert_to_merge为off
drop table if exists products5;
--建表，指定一列是主键
CREATE TABLE products5 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规insert插入一条数据
insert into  products5 values(01,'grains',5.5);
select * from  products5;
--使用insert...update插入一条数据，主键不重复，update product_no 列，合理报错
insert into  products5 values(02,'veggies',6.8) on DUPLICATE key update product_no='02';
select * from  products5;
drop table products5;