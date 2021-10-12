--  @testpoint:创建表时指定其中一列是主键约束,主键约束上常规插入重复值，合理报错
drop table if exists products1;
--建表指定一列是主键
CREATE TABLE products1 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
insert into  products1 values(01,'grains',5.5);
select * from products1;
--主键约束上常规插入重复值
insert into  products1 values(01,'grains',5.5);
drop table products1;
