-- @testpoint: pg_stat_get_tuples_hot_updated(oid)返回表里热更新的行数
alter system set autovacuum to off;
drop table if exists sales;
drop table if exists sales1;
select pg_stat_reset();
-- 建索引，update不会记录
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
-- 未插入数据，在创建索引前后查
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_hot_updated(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 数据插入sales
INSERT INTO sales VALUES(1, 12, '2019-01-10 00:00:00', 'a', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-01 00:00:00', 'b', 1, 1, 1);
create index test_index on sales(time_id); -- 索引必须和所更新行一致才不糊记录
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_hot_updated(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 索引更新一条 0
update sales set time_id = '2017-12-10 00:00:00' where channel_id = 'a';
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_hot_updated(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 索引一条更新多次 0
update sales set time_id = '2019-06-02 10:00:00' where channel_id = 'b';
update sales set time_id = '2019-06-03 10:00:00' where channel_id = 'b';
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_hot_updated(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 非索引更新一条 会记录 1
update sales set amount_sold = 3 where channel_id = 'a';
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_hot_updated(a.oid) from PG_CLASS a where a.relname = 'sales';
drop table sales cascade;
-- 无索引
--创建表sales1
CREATE TABLE sales1
(prod_id NUMBER(6),
 cust_id NUMBER,
 time_id DATE,
 channel_id CHAR(1),
 promo_id NUMBER(6),
 quantity_sold NUMBER(3),
 amount_sold NUMBER(10,2)
);
-- 未插入数据查询
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_hot_updated(a.oid) from PG_CLASS a where a.relname = 'sales1';
-- 数据插入sales1
INSERT INTO sales1 VALUES(1, 12, '2019-01-10 00:00:00', 'a', 1, 1, 1);
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_hot_updated(a.oid) from PG_CLASS a where a.relname = 'sales1';
INSERT INTO sales1 VALUES(1, 12, '2019-02-01 00:00:00', 'b', 1, 1, 1);
INSERT INTO sales1 VALUES(1, 12, '2019-02-05 00:00:00', 'c', 1, 1, 1);
INSERT INTO sales1 VALUES(1, 12, '2019-02-03 00:00:00', 'd', 1, 1, 1);
INSERT INTO sales1 VALUES(1, 12, '2019-02-05 00:00:00', 'e', 1, 1, 1);
-- 更新一条 1
update sales1 set time_id = '2017-12-10 00:00:00' where channel_id = 'a';
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_hot_updated(a.oid) from PG_CLASS a where a.relname = 'sales1';
-- 一条更新多次 3
update sales1 set time_id = '2019-06-02 10:00:00' where channel_id = 'b';
update sales1 set time_id = '2019-06-03 10:00:00' where channel_id = 'b';
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_hot_updated(a.oid) from PG_CLASS a where a.relname = 'sales1';
-- 更新多条 6
update sales1 set time_id = '2019-06-01 10:00:00' where channel_id = 'c';
update sales1 set time_id = '2019-06-02 10:00:00' where channel_id = 'd';
update sales1 set time_id = '2019-06-03 10:00:00' where channel_id = 'e';
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_tuples_hot_updated(a.oid) from PG_CLASS a where a.relname = 'sales1';
drop table sales1 cascade;
alter system set autovacuum to on;