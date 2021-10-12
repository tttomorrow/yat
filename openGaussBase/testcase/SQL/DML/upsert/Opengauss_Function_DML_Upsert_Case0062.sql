--  @testpoint:使用insert...nothing语句，给主键列插入null值，合理报错
--预置条件enable_upsert_to_merge为off
drop table if exists products_c6;
--建表，指定一列是主键
CREATE TABLE products_c6 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规插入一条数据
insert into  products_c6 values(10,'grains',5.5);
select * from  products_c6;
--使用insert...nothing语句,给主键列插入null值
insert into products_c6( name,price) values('grains1',5.25) on DUPLICATE key update nothing;
--给主键列插入null值
insert into products_c6 values(null,'grains1',5.25) on DUPLICATE key update nothing;
select * from  products_c6;
drop table products_c6;