--  @testpoint:使用insert...update语句插入一条数据，添加EXCLUDED关键字，主键列数据已存在，其他列数据已存在
----预置条件enable_upsert_to_merge为off
drop table if exists products27;
--建表，指定一列是主键
CREATE TABLE products27 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规插入一条数据
insert into  products27 values(10,'grains',5.5);
select * from  products27;
--添加EXCLUDED关键字,主键重复，update name列和price列,数据未发生变化
insert into  products27 values(10,'grains',5.5) on DUPLICATE key update name=EXCLUDED.name, price =EXCLUDED.price;
select * from  products27;
drop table products27;