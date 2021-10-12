-- @testpoint: pg_stat_get_tuples_deleted(oid)返回从表中删除行的数量。
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
SELECT pg_sleep(1);
select pg_stat_get_tuples_deleted(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 数据插入
INSERT INTO sales VALUES(1, 12, '2017-01-10 00:00:00', 'a', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-05-01 10:00:00', 'b', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-05-01 10:00:00', 'c', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-05-01 10:00:00', 'd', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-05-01 10:00:00', 'e', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-05-01 10:00:00', 'f', 1, 1, 1);
SELECT pg_sleep(1);
select pg_stat_get_tuples_deleted(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 删除一行 1
delete  from  sales  where channel_id = 'a';
SELECT pg_sleep(1);
select pg_stat_get_tuples_deleted(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 删除两行一样的  2
delete  from  sales  where channel_id = 'b';
delete  from  sales  where channel_id = 'b';
SELECT pg_sleep(1);
select pg_stat_get_tuples_deleted(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 删除多行 5
delete  from  sales  where channel_id = 'd';
delete  from  sales  where channel_id = 'e';
delete  from  sales  where channel_id = 'f';
SELECT pg_sleep(1);
select pg_stat_get_tuples_deleted(a.oid) from PG_CLASS a where a.relname = 'sales';
drop table sales cascade;
alter system set autovacuum to on;