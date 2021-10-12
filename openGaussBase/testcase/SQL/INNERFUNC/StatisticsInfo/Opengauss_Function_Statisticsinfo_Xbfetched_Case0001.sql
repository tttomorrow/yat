-- @testpoint: pg_stat_get_xact_blocks_fetched(oid)返回当前事务中对表或索引的磁盘块获取请求数。
alter system set autovacuum to off;
drop table if exists sales;
select pg_stat_reset();
begin;
/
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
-- 创建索引前查询 0
SELECT pg_sleep(1);
select pg_stat_get_xact_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 创建索引 0 0
create index test_index1 on sales (channel_id);
SELECT pg_sleep(1);
select pg_stat_get_xact_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'test_index1';
-- 数据插入sales  1 2
INSERT INTO sales VALUES(1, 12, '2019-02-01 00:00:00', 'b', 1, 1, 1);
SELECT pg_sleep(1);
select pg_stat_get_xact_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'test_index1';
-- 更新一行数据 0 0
update sales set time_id = '2019-06-02 10:00:00' where channel_id = 'b';
SELECT pg_sleep(1);
select pg_stat_get_xact_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'test_index1';
-- 再添加数据
INSERT INTO sales VALUES(1, 12, '2019-02-05 00:00:00', 'c', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-03 00:00:00', 'd', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-05 00:00:00', 'e', 1, 1, 3);
SELECT pg_sleep(1);
select pg_stat_get_xact_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'test_index1';
-- 更新多行
update sales set time_id = '2015-06-02 10:00:00' where channel_id = 'c';
update sales set time_id = '2013-06-02 10:00:00' where channel_id = 'd';
update sales set time_id = '2012-06-02 10:00:00' where amount_sold = 3;
SELECT pg_sleep(1);
select pg_stat_get_xact_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'test_index1';
-- 删除一行
delete from sales where channel_id = 'b';
select pg_stat_get_xact_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'test_index1';
-- 删除多行
delete from sales where channel_id = 'c';
delete from sales where channel_id = 'd';
delete from sales where channel_id = 'e';
SELECT pg_sleep(1);
select pg_stat_get_xact_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'test_index1';
-- 清计数 0 0
select pg_stat_reset();
SELECT pg_sleep(1);
select pg_stat_get_xact_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'test_index1';
-- 0 0
select * from sales;
SELECT pg_sleep(1);
select pg_stat_get_xact_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'test_index1';
drop table sales cascade;
end;
alter system set autovacuum to on;