--  @testpoint:创建表时指定其中一列是主键约束,主键约束上常规插入不同值，正常插入

drop table if exists products;
--建表指定一列是主键
CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--主键约束上常规插入不同值
insert into  products values(01,'grains',5.5),(02,'veggies',6.5);
select * from products;
drop table products;