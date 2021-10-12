--  @testpoint:先使用insert...update语句，再使用常规insert语句
--预置条件enable_upsert_to_merge为off
drop table if exists products15;
--建表，指定一列是主键
CREATE TABLE products15 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规插入一条数据
insert into  products15 values(110,'meat',22.5);
select * from products15;
--主键冲突，使用insert...update插入一条数据，upadte name列,数据(110,'meat',22.5)更改为(110,'orange',22.5)
insert into  products15 values(110,'orange',7.4) on DUPLICATE key update name='orange';
select * from products15;
--使用常规insert语句再插一条数据，主键不重复，插入成功
insert into  products15 values(111,'orange',7.4) ;
select * from products15;
drop table products15;