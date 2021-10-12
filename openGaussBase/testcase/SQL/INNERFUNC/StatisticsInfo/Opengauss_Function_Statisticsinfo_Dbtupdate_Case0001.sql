-- @testpoint: pg_stat_get_db_tuples_updated(oid)返回在数据库中更新的Tuple数
alter system set autovacuum to off;
drop table if exists sales;
select pg_stat_reset();
select pg_sleep(2);
select pg_stat_get_db_tuples_updated(a.oid)=0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
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
select pg_sleep(2);
select pg_stat_get_db_tuples_updated(a.oid) from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- 数据插入sales
INSERT INTO sales VALUES(1, 12, '2019-01-10 00:00:00', 'a', 1, 1, 1);
select pg_sleep(2);
select pg_stat_get_db_tuples_updated(a.oid) from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- 数据插入sales
INSERT INTO sales VALUES(1, 12, '2019-02-01 00:00:00', 'b', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-05 00:00:00', 'c', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-03 00:00:00', 'd', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-05 00:00:00', 'e', 1, 1, 1);
-- 更新一条
update sales set time_id = '2019-06-02 10:00:00' where channel_id = 'a';
select pg_sleep(2);
select pg_stat_get_db_tuples_updated(a.oid) from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- 一条更新多次
update sales set time_id = '2019-06-02 10:00:00' where channel_id = 'b';
update sales set time_id = '2019-06-02 10:00:00' where channel_id = 'b';
select pg_sleep(2);
select pg_stat_get_db_tuples_updated(a.oid) from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- 更新多条
update sales set time_id = '2019-06-01 10:00:00' where channel_id = 'c';
update sales set time_id = '2019-06-02 10:00:00' where channel_id = 'd';
update sales set time_id = '2019-06-03 10:00:00' where channel_id = 'e';
select pg_sleep(2);
select pg_stat_get_db_tuples_updated(a.oid) from PG_DATABASE a where a.datname = CURRENT_CATALOG;
drop table sales cascade;
alter system set autovacuum to on;
