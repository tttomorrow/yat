--  @testpoint:使用upsert语句给主键约束插入null值，合理报错
--预置条件enable_upsert_to_merge为off
drop table if exists products14;
--建表，指定一列是主键
CREATE TABLE products14 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);

--使用insert...update插入一条数据,主键列插入null值
insert into  products14(name,price) values('orange',7.4) on DUPLICATE key update name='orange';
--主键列插入null值
insert into  products14 values(null,'orange',7.4) on DUPLICATE key update name='orange';
drop table products14;