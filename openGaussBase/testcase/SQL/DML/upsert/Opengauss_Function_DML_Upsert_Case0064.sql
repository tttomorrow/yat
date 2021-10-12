--  @testpoint:使用insert..nothing插入一条语句，执行该语句两次
--预置条件enable_upsert_to_merge为off
drop table if exists products_c8;
--建表，指定一列是主键
CREATE TABLE products_c8 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规插入一条数据
insert into  products_c8 values(10,'grains',5.5);
select * from  products_c8;
--使用insert...nothing语句，主键不重复，其他列数据不重复，新增一条数据(9,'veggies2',6.88)
insert into  products_c8 values (9,'veggies2',6.88) on DUPLICATE key update nothing;
select * from  products_c8;
--再次执行以上语句，直接返回
insert into  products_c8 values (9,'veggies2',6.88) on DUPLICATE key update nothing;
drop table products_c8;