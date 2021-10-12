--  @testpoint:使用insert...update语句插入一条数据，主键列数据不存在，其他列数据已存在，新插入一条数据
--预置条件enable_upsert_to_merge为off
drop table if exists products3;
CREATE TABLE products3 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--insert常规插入一条数据
insert into  products3 values(01,'grains',5.5);
select * from products3;
--使用insert...update插入一条数据，主键不重复，update后跟name列，新增一条数据(02,'grains',5.5)
insert into  products3 values(02,'grains',5.5) on DUPLICATE key update name='grains';
select * from products3;
drop table products3;
