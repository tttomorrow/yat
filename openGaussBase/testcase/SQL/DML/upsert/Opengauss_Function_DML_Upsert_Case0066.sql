--  @testpoint:事务中，使用upsert语句，再rollback
--预置条件enable_upsert_to_merge为off
drop table if exists products_c10;
--建表，指定一列是主键
CREATE TABLE products_c10 (
    product_no integer primary key,
    name text,
    price numeric
);
--常规插入一条数据
insert into  products_c10 values(10,'grains',5.5);
select * from  products_c10;
----使用insert...nothing语句，主键不重复，其他列数据不重复，新增一条数据(9,'veggies2',6.88)
start transaction;
insert into  products_c10 values (9,'veggies2',6.88) on DUPLICATE key update nothing;
select * from  products_c10;
--回退到使用insert...nothing语句之前的数据(10,'grains',5.5)
rollback;
select * from  products_c10;
start transaction;
--使用insert..update语句，数据更新为(10,'apple',6.88)
insert into  products_c10 values (10,'apple',6.88) on DUPLICATE key update name='apple',price=6.88;
select * from  products_c10;
--使用insert..update..excluded语句,数据更新为(10,'apple1',6.58)且新增一条数据(11,'grape',4.5)
insert into  products_c10 values (10,'apple1',6.58),(11,'grape',4.5)ON DUPLICATE key update  name=excluded.name,price=excluded.price;
select * from  products_c10;
--回退
rollback;
--数据回到(10,'grains',5.5)
select * from  products_c10;
drop table products_c10;