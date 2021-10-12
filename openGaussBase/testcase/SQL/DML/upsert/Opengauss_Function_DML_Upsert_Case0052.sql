--  @testpoint:事务中，使用insert...update语句并添加关键字EXCLUDED，再使用rollback
----预置条件enable_upsert_to_merge为off
drop table if exists products_b5;
--建表，指定一列是主键
CREATE TABLE products_b5 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规insert插入一条数据
insert into  products_b5 values(01,'grains',5.5);
select * from  products_b5;
--使用insert...update语句插入一条数据，主键重复，upadte name列的值为'meat'
start transaction;
insert into  products_b5 values(01,'meat',22.8) on DUPLICATE key update name=EXCLUDED.name;
select * from  products_b5;
--使用rollback
rollback;
--products_b5和使用insert...update语句前一样，name列值恢复为'grains'
select * from  products_b5;
drop table products_b5;