-- @testpoint: pg_stat_get_db_tuples_deleted(oid)返回数据库中删除的Tuple数。
alter system set autovacuum to off;
drop table if exists sales;
select pg_stat_reset();
SELECT pg_sleep(2);
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
select pg_stat_get_db_tuples_deleted(a.oid) from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- 数据插入
INSERT INTO sales VALUES(1, 12, '2017-01-10 00:00:00', 'a', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-05-01 10:00:00', 'b', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-05-01 10:00:00', 'c', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-05-01 10:00:00', 'd', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-05-01 10:00:00', 'e', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-05-01 10:00:00', 'f', 1, 1, 1);
select pg_stat_get_db_tuples_deleted(a.oid) from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- 删除一行
delete from sales where channel_id = 'a';
SELECT pg_sleep(3);
select pg_stat_get_db_tuples_deleted(a.oid) from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- 删除多行
delete from sales where channel_id = 'b';
delete from sales where channel_id = 'c';
delete from sales where channel_id = 'd';
delete from sales where channel_id = 'e';
delete from sales where channel_id = 'f';
SELECT pg_sleep(4);
select pg_stat_get_db_tuples_deleted(a.oid) from PG_DATABASE a where a.datname = CURRENT_CATALOG;
drop table sales cascade;
alter system set autovacuum to on;