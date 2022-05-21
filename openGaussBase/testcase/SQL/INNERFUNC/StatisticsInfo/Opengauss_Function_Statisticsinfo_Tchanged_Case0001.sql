-- @testpoint: pg_stat_get_tuples_changed(oid)返回该表上一次analyze或autoanalyze之后插入、更新、删除行的总数量。
alter system set autovacuum to off;
drop table if exists sales;
select pg_stat_reset();
SELECT pg_sleep(6);
SELECT pg_sleep(6);
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
-- 未插入数据未analyse 0
select pg_stat_get_tuples_changed(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 未插入数据先analyse 0
ANALYZE sales;
select pg_stat_get_tuples_changed(a.oid) from PG_CLASS a where a.relname = 'sales';
-- analyse 后插入数据 1
INSERT INTO sales VALUES(1, 12, '2019-01-10 00:00:00', 'a', 1, 1, 1);
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_changed(a.oid) from PG_CLASS a where a.relname = 'sales';
-- analyse 后插入多行数据 2 5
INSERT INTO sales VALUES(1, 12, '2019-02-01 00:00:00', 'b', 1, 1, 1);
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_changed(a.oid) from PG_CLASS a where a.relname = 'sales';
INSERT INTO sales VALUES(1, 12, '2019-02-05 00:00:00', 'c', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-03 00:00:00', 'd', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-05 00:00:00', 'e', 1, 1, 1);
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_changed(a.oid) from PG_CLASS a where a.relname = 'sales';
-- analyse 后更新一条 6
update sales set time_id = '2017-12-10 00:00:00' where channel_id = 'a';
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_changed(a.oid) from PG_CLASS a where a.relname = 'sales';
-- analyse 后一条更新多次 8
update sales set time_id = '2019-06-02 10:00:00' where channel_id = 'b';
update sales set time_id = '2019-06-02 10:00:00' where channel_id = 'b';
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_changed(a.oid) from PG_CLASS a where a.relname = 'sales';
-- analyse 后更新多条 11
update sales set time_id = '2019-06-01 10:00:00' where channel_id = 'c';
update sales set time_id = '2019-06-02 10:00:00' where channel_id = 'd';
update sales set time_id = '2019-06-03 10:00:00' where channel_id = 'e';
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_changed(a.oid) from PG_CLASS a where a.relname = 'sales';
-- analyse 后删除一行 12
delete  from  sales  where channel_id = 'a';
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_changed(a.oid) from PG_CLASS a where a.relname = 'sales';
-- analyse 后删除两行 14
delete  from  sales  where channel_id = 'b';
delete  from  sales  where channel_id = 'c';
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_changed(a.oid) from PG_CLASS a where a.relname = 'sales';
-- analyse 后删除多行 f不存在，不增加 16
delete  from  sales  where channel_id = 'd';
delete  from  sales  where channel_id = 'e';
delete  from  sales  where channel_id = 'f';
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_changed(a.oid) from PG_CLASS a where a.relname = 'sales';
drop table sales cascade;
alter system set autovacuum to on;