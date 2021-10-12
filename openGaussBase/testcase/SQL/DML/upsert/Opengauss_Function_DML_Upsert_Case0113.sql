--  @testpoint:使用insert...update语句插入一条数据,主键列数据已存在，其他列数据已存在，update主键列，合理报错
--预置条件enable_upsert_to_merge为off
drop table if exists products10;
--建表，指定一列是主键
CREATE TABLE products10 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--insert常规插入一条数据
insert into  products10 values(01,'grains',5.5);
select * from  products10;
--使用insert...update插入一条数据，update product_no，合理报错
insert into  products10 values(01,'grains',5.5) on DUPLICATE key update product_no=01;
select * from  products10;
drop table products10;