--  @testpoint:使用SET CONSTRAINTS语句设置当前事务检查行为的约束条件（外键约束）
--创建主键表
drop table if exists products;
--建表，指定一列是主键
create table products(
products_no integer primary key,
name varchar(50),
price numeric
);
--插入数据
insert into products values(1,'a',8.9);
--创建外键表，指定外键orders.products_no和products.products_no是外键和主键的关系
drop table if exists orders;
create table  orders(
order_id integer  primary key ,
products_no integer references products(products_no),
quantity integer
);

--开启事务
start transaction;
--设置约束为immediate
set CONSTRAINTS all immediate;
--给外键表插入数据,合理报错
insert into orders values(2,3,100);
end;
--开启事务
start transaction;
--设置约束为DEFERRED
set CONSTRAINTS all DEFERRED;
--给外键表插入数据,合理报错
insert into orders values(2,3,100);
end;
--删表
drop table products cascade;
drop table orders cascade;