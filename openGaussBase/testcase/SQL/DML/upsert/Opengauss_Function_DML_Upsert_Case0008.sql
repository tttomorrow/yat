--  @testpoint:使用insert...update语句插入一条数据,主键列数据不存在，其他列数据不存在，新插入一条数据
----预置条件enable_upsert_to_merge为off
drop table if exists products5;
CREATE TABLE products5 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规insert插入一条数据
insert into  products5 values(01,'grains',5.5);
select * from  products5;
--使用insert...update插入一条数据，主键不重复，update name 列,新增一条数据(02,'veggies',6.8)
insert into  products5 values(02,'veggies',6.8) on DUPLICATE key update name='veggies';
select * from  products5;
drop table products5;