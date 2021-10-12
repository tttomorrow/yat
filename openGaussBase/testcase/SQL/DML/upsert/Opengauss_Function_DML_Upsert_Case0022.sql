--  @testpoint:事务中，使用insert...update语句，再使用rollback
--预置条件enable_upsert_to_merge为off
drop table if exists products19;
--建表，指定一列是主键
CREATE TABLE products19 (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
--常规insert插入一条数据
insert into  products19 values(01,'grains',5.5);
select * from  products19;
--使用insert...update语句插入一条数据，主键重复，upadte name列，数据(01,'grains',5.5)更改为(01,'meat',5.5)
start transaction;
insert into  products19 values(01,'meat',22.8) on DUPLICATE key update name='meat';
select * from  products19;
--使用rollback
rollback;
--products19表数据和使用insert...update语句前一样，数据是(01,'grains',5.5)
select * from  products19;
--commit后再执行rollback
start transaction;
--使用insert...update语句插入一条数据，主键重复，upadte name列，数据(01,'grains',5.5)更改为(01,'meat',5.5)
insert into  products19 values(01,'meat',22.8) on DUPLICATE key update name='meat';
select * from  products19;
commit;
rollback;
--数据仍是(01,'meat',5.5)
select * from  products19;
drop table products19;