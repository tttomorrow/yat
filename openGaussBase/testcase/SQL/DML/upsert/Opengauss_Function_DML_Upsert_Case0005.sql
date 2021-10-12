--  @testpoint:创建表时指定其中一列是主键约束,主键约束上常规插入null值，合理报错
drop table if exists products2;
--建表指定一列是主键
CREATE TABLE products2 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--主键约束上常规插入null值
insert into  products2(name, price) values('grains',5.5);
--主键约束上常规插入null值
insert into  products2 values(null,'grains',5.5);
drop table products2;
