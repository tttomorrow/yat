--  @testpoint:使用insert...update语句插入一条数据，添加EXCLUDED关键字，主键列数据不存在，其他列数据不存在，新插入一条数据成功
drop table if exists products32;
CREATE TABLE products32 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规插入一条数据
insert into  products32 values(10,'grains',5.5);
select * from  products32;
--添加EXCLUDED关键字,主键列不重复，update  name 列，新插入一条数据成功
insert into  products32 values(11,'apple',6.2) on DUPLICATE key update name=EXCLUDED.name;
select * from  products32;
drop table products32;