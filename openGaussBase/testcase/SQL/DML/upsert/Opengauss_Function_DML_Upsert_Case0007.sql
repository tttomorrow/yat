--  @testpoint:使用insert...update语句插入一条数据,主键列数据不存在，其他列数据已存在，update主键列，合理报错
----预置条件enable_upsert_to_merge为off
drop table if exists products4;
CREATE TABLE products4 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规insert插入一条数据
insert into  products4 values(01,'grains',5.5);
select * from  products4;
--使用insert...update插入一条数据，主键不重复，update  product_no列,合理报错
insert into  products4 values(02,'grains1',5.5) on DUPLICATE key update  product_no='01';
select * from  products4;
drop table products4;
