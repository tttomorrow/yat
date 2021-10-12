--  @testpoint:先使用insert...update语句，再使用常规insert语句
--预置条件enable_upsert_to_merge为off
drop table if exists products16;
--建表，指定一列是主键
CREATE TABLE products16 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
insert into  products16 values(10,'meat',22.5);
select * from products16;
--主键冲突，使用insert...update插入一条数据，数据(10,'meat',22.5)更改为(10,'orange',22.5)
insert into  products16 values(10,'orange',7.4) on DUPLICATE key update name='orange';
select * from products16;
--使用常规inse语句再插一条数据，主键重复，合理报错
insert into  products16 values(10,'oil',1.8) ;
select * from products16;
drop table products16;