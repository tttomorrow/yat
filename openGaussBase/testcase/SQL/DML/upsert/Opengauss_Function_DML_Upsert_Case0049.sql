--  @testpoint:先使用insert...update语句，添加关键字EXCLUDED，再使用常规insert语句，再使用insert...update语句
----预置条件enable_upsert_to_merge为off
drop table if exists products_b2;
--建表，指定一列是主键
CREATE TABLE products_b2 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规插入一条数据
insert into  products_b2 values(110,'meat',22.5);
select * from products_b2;
--主键冲突，使用insert...update插入一条数据，upadte name列,name列更改为'orange'
insert into  products_b2 values(110,'orange',7.4) on DUPLICATE key update name=EXCLUDED.name;
select * from products_b2;
--使用常规insert语句再插一条数据，主键不重复，插入成功
insert into  products_b2 values(111,'orange',7.4) ;
select * from products_b2;
--使用insert...update插入一条数据,不加关键字EXCLUDED，数据(110,'orange',22.5)改为(110,'apple',22.5)
insert into products_b2 values(110,'orange',7.4) ON DUPLICATE key update  name='apple';
select * from products_b2;
drop table products_b2;