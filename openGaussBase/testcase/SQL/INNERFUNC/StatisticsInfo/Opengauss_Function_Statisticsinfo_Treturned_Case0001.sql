-- @testpoint: pg_stat_get_tuples_returned(oid)返回顺序扫描读取的行数目或索引行的数目。
-- 清理环境
alter system set autovacuum to off;
drop table if exists sales;
select pg_stat_reset();
--创建表sales
CREATE TABLE sales
(prod_id numeric(6),
 cust_id numeric,
 time_id DATE,
 channel_id CHAR(1),
 promo_id numeric(6),
 quantity_sold numeric(3),
 amount_sold numeric(10,2)
);
create index test_index1 on sales(prod_id);
-- 清除后新建表初始0
select pg_stat_get_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index1';
-- 数据插入不会return
-- 数据插入sales
INSERT INTO sales VALUES(1, 12, '2019-01-10 00:00:00', 'a', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-01 00:00:00', 'b', 1, 1, 1);
select pg_stat_get_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index1';
-- 验证查表返回
--查表 返回两行2 0
SELECT * FROM sales;
SELECT pg_sleep(1);
select pg_stat_get_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index1';
-- testpoint:验证进索引返回
-- 进入索引 也返回两行2 2  2 4
update sales set time_id = '2019-06-02 10:00:00' where prod_id = 1;
SELECT pg_sleep(1);
select pg_stat_get_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index1';

update sales set time_id = '2020-06-02 10:00:00' where prod_id = 1;
SELECT pg_sleep(1);
select pg_stat_get_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index1';
-- testpoint:创建索引引起全局扫描 8 4 0  10 4 0
create index test_index2 on sales (cust_id);
SELECT pg_sleep(10);
select pg_stat_get_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index1';
select pg_stat_get_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index2';

update sales set channel_id = 'H' where cust_id = 12;
SELECT pg_sleep(3);
select pg_stat_get_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index1';
select pg_stat_get_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index2';

-- 查询所有 cust_id=12  channel_id:abc
SELECT * FROM sales;
SELECT * FROM sales where prod_id = 1;
SELECT pg_sleep(2);
select pg_stat_get_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index1';
select pg_stat_get_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index2';
-- testpoint:查询不存在的
SELECT * FROM sales where cust_id = 1;
SELECT * FROM sales where channel_id = 'g';
SELECT pg_sleep(1);
select pg_stat_get_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index1';
select pg_stat_get_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index2';
-- 恢复环境
drop table sales cascade;
alter system set autovacuum to on;