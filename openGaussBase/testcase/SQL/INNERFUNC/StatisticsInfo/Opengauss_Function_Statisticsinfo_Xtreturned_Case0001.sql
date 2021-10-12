-- @testpoint: pg_stat_get_xact_tuples_returned(oid)返回当前事务中通过顺序扫描读取的行数或索引条目数。
alter system set autovacuum to off;
drop table if exists sales;
select pg_stat_reset();
SELECT pg_sleep(1);
--创建表sales
CREATE TABLE sales
(prod_id NUMBER(6),
 cust_id NUMBER,
 time_id DATE,
 channel_id CHAR(1),
 promo_id NUMBER(6),
 quantity_sold NUMBER(3),
 amount_sold NUMBER(10,2)
);
create index test_index1 on sales(prod_id);
begin;
/
select pg_stat_get_xact_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index1';
-- 数据插入sales
INSERT INTO sales VALUES(1, 12, '2019-01-10 00:00:00', 'a', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-01 00:00:00', 'b', 1, 1, 1);
select pg_stat_get_xact_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index1';
--查表 返回两行2 0
SELECT * FROM sales;
SELECT pg_sleep(1);
select pg_stat_get_xact_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index1';
-- 进入索引 也返回两行2 2  2 4
update sales set time_id = '2019-06-02 10:00:00' where prod_id = 1;
SELECT pg_sleep(1);
select pg_stat_get_xact_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index1';
update sales set time_id = '2020-06-02 10:00:00' where prod_id = 1;
SELECT pg_sleep(1);
select pg_stat_get_xact_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index1';
--创建索引会引起全局的扫描 8 4 0  10 4 0
create index test_index2 on sales (cust_id);
SELECT pg_sleep(1);
select pg_stat_get_xact_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index1';
select pg_stat_get_xact_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index2';
update sales set channel_id = 'H' where cust_id = 12;
SELECT pg_sleep(1);
select pg_stat_get_xact_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index1';
select pg_stat_get_xact_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index2';
-- 查询所有 cust_id=12  channel_id:abc
SELECT * FROM sales;
SELECT * FROM sales where prod_id = 1;
SELECT pg_sleep(1);
select pg_stat_get_xact_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index1';
SELECT * FROM sales where cust_id = 1;
SELECT * FROM sales where channel_id = 'g';
SELECT pg_sleep(1);
select pg_stat_get_xact_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index2';
-- 事务外进行查询
end;
select pg_stat_get_xact_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index1';
select pg_stat_get_xact_tuples_returned(a.oid) from PG_CLASS a where a.relname = 'test_index2';
drop table sales cascade;
alter system set autovacuum to on;