-- @testpoint: pg_stat_get_tuples_inserted(oid)返回插入表中行的数量。
alter system set autovacuum to off;
drop table if exists sales;
select pg_stat_reset();
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
select pg_stat_get_tuples_inserted(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 数据插入sales 1
INSERT INTO sales VALUES(1, 12, '2019-01-10 00:00:00', 'a', 1, 1, 1);
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_inserted(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 数据插入sales 2
INSERT INTO sales VALUES(1, 12, '2019-02-01 00:00:00', 'b', 1, 1, 1);
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_inserted(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 再添加数据 6
INSERT INTO sales VALUES(1, 12, '2019-02-05 00:00:00', 'c', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-03 00:00:00', 'd', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-05 00:00:00', 'e', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-03 00:00:00', 'f', 1, 1, 1);
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_inserted(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 删除数据  6 不会影响，因为记录的是insert的次数
delete  from  sales  where amount_sold = 1;
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_inserted(a.oid) from PG_CLASS a where a.relname = 'sales';
drop table sales cascade;
alter system set autovacuum to on;