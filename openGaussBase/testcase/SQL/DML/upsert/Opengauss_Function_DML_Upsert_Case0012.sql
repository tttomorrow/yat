--  @testpoint:使用insert...update语句插入一条数据,主键列数据已存在，其他列数据已存在，update name 列，数据未发生变化
--预置条件enable_upsert_to_merge为off
drop table if exists products9;
--建表，指定一列是主键
CREATE TABLE products9 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规insert插入一条数据
insert into  products9 values(01,'grains',5.5);
select * from  products9;
--使用insert...update插入一条数据，update name 列，更新0条数据
insert into  products9 values(01,'grains',5.5) on DUPLICATE key update name='grains';
select * from  products9;
drop table products9;