--  @testpoint:主键和外键结合，使用insert..update语句
--预置条件enable_upsert_to_merge为off
drop table if exists products;
--建表，指定一列是主键
create table products(
products_no integer primary key,
name varchar(50),
price numeric
);
--创建表，指定外键orders，orders.products_no和products.products_no是外键和主键的关系
drop table if exists orders;
create table  orders(
order_id integer  primary key ,
products_no integer references products(products_no),
quantity integer
);
--给主键表插入两条数据，主键不重复，新增两条数据
insert into products values(1,'a',5.2),(2,'b',2.8)  on DUPLICATE key update name='a';
select * from products;
--给外键表插入两条数据，外键重复，合理报错，外键值必须在主键中
insert into orders values(1,10,50),(2,10,20)  on DUPLICATE key update quantity=20;

--给外键表插入两条数据，外键值是主键表products_no列的值，新增两条数据
insert into orders values(10,1,50),(11,2,20)  on DUPLICATE key update quantity=20;
select * from orders;
--给外键表插入两条数据，orders.products_no和products.products_no重复，新增两条数据
insert into orders values(1,1,50),(2,2,20)  on DUPLICATE key update quantity=20;
select * from orders;
drop table products cascade;
drop table orders;