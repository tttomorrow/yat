-- @testpoint: 使用insert...update语句，添加where条件选择性更新
--预置条件enable_upsert_to_merge为off
drop table if exists products20;
--建表，指定一列是主键
CREATE TABLE products20 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规插入一条数据
insert into  products20 values(10,'grains',5.5);
select * from  products20;
--添加where条件，由于product_no没有大于10的数据，故更新0条数据
insert into  products20 values(10,'meat',22.8) on DUPLICATE key update name='meat' where products20.product_no >10;
select * from  products20;
drop table products20;