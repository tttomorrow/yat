-- @testpoint: pg_stat_get_xact_numscans(oid)返回当前事务中执行的顺序扫描次数或索引扫描次数。
alter system set autovacuum to off;
drop table if exists sales;
drop table if exists products;
CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text
);
insert into products values (1,'a');
begin;
/
CREATE TABLE sales (
 product_no numeric(6),
 cust_id numeric,
 time_id DATE,
 channel_id CHAR(1),
 promo_id numeric(6),
 quantity_sold numeric(3),
 amount_sold numeric(10,2)
);
select pg_stat_get_xact_numscans(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 查表 1 0
SELECT * FROM sales;
SELECT pg_sleep(1);
select pg_stat_get_xact_numscans(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_numscans(a.oid) from PG_CLASS a where a.relname = 'test_index1';
-- 创建索引 2 0
create index test_index1 on sales (cust_id);
SELECT pg_sleep(1);
select pg_stat_get_xact_numscans(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_numscans(a.oid) from PG_CLASS a where a.relname = 'test_index1';
-- 添加外键 3 0
alter table sales add constraint product_no foreign key(product_no) REFERENCES products(product_no);
SELECT pg_sleep(1);
select pg_stat_get_xact_numscans(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_numscans(a.oid) from PG_CLASS a where a.relname = 'test_index1';
-- 插入数据 3 0
INSERT INTO sales VALUES(1, 12, '2019-01-10 00:00:00', 'a', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-01 00:00:00', 'b', 1, 1, 1);
SELECT pg_sleep(1);
select pg_stat_get_xact_numscans(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_numscans(a.oid) from PG_CLASS a where a.relname = 'test_index1';
-- 更新数据 3 1
update sales set channel_id = 'H' where cust_id = 12;
SELECT pg_sleep(1);
select pg_stat_get_xact_numscans(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_numscans(a.oid) from PG_CLASS a where a.relname = 'test_index1';
-- 添加数据 3 1
INSERT INTO sales VALUES(1, 12, '2019-02-01 00:00:00', 'c', 1, 1, 1);
SELECT pg_sleep(1);
select pg_stat_get_xact_numscans(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_numscans(a.oid) from PG_CLASS a where a.relname = 'test_index1';
-- 删除数据 4 1
delete from sales where channel_id = 'b';
SELECT pg_sleep(1);
select pg_stat_get_xact_numscans(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_numscans(a.oid) from PG_CLASS a where a.relname = 'test_index1';
-- 删除索引 4
drop index test_index1;
SELECT pg_sleep(1);
select pg_stat_get_xact_numscans(a.oid) from PG_CLASS a where a.relname = 'sales';
drop table sales cascade;
drop table products cascade;
end;
alter system set autovacuum to on;