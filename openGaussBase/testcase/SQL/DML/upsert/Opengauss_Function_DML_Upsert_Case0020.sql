--  @testpoint:冲突后使用insert...update执行同样语句两次
--预置条件enable_upsert_to_merge为off
drop table if exists products17;
--建表，指定一列是主键
CREATE TABLE products17 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规insert插入一条数据
insert into  products17 values(01,'grains',5.5);
select * from products17;
--使用insert...update语句插入一条数据，主键不重复，插入数据成功
insert into  products17 values(02,'grains',5.5) on DUPLICATE key update name='grains', price=5.5;
select * from products17;
--再次执行以上语句，不报错，数据未发生变化
insert into  products17 values(02,'grains',5.5) on DUPLICATE key update name='grains', price=5.5;
select * from  products17;
drop table products17;