--  @testpoint:插入一条数据，结合使用insert..update，insert...nothing语句
--预置条件enable_upsert_to_merge为off
drop table if exists products_c7;
--建表，指定一列是主键
CREATE TABLE products_c7 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规插入一条数据
insert into  products_c7 values(10,'grains',5.5);
select * from  products_c7;
--使用insert..update语句，主键重复，其他列数据不重复，修改数据(10,'grains',5.5)为(10,'veggies',5.5)
insert into  products_c7 values(10,'veggies',6.8) on DUPLICATE key update name='veggies';
select * from  products_c7;
--使用insert..update语句并加关键字EXCLUDED，主键重复，其他列数据不重复,修改数据(10,'veggies',5.5)为(10,'veggies1',6.8)
insert into  products_c7 values (10,'veggies1',6.8) on DUPLICATE key update name=EXCLUDED.name,price=EXCLUDED.price;
select * from  products_c7;
--使用insert...nothing语句，主键重复，其他列数据不重复，直接返回
insert into  products_c7 values (10,'veggies2',6.88) on DUPLICATE key update nothing;
select * from  products_c7;
drop table products_c7;