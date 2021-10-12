-- @testpoint: pg_stat_get_db_tuples_inserted(oid)返回在数据库中插入的Tuple数。
alter system set autovacuum to off;
drop table if exists sales;
drop table if exists sales1;
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
-- 会有系统表的存在
select pg_stat_get_db_tuples_inserted(a.oid)=0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- 数据插入sales
INSERT INTO sales VALUES(1, 12, '2019-01-10 00:00:00', 'a', 1, 1, 1);
SELECT pg_sleep(1);
select pg_stat_get_db_tuples_inserted(a.oid)>0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_tuples_inserted(a.oid)=0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- 数据插入sales
INSERT INTO sales VALUES(1, 12, '2019-02-01 00:00:00', 'b', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-01 00:00:00', 'c', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-01 00:00:00', 'd', 1, 1, 1);
SELECT pg_sleep(1);
select pg_stat_get_db_tuples_inserted(a.oid)>0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_tuples_inserted(a.oid)=0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- 删除数据,不会变，计的是insert了多少次
delete from sales where amount_sold=1;
SELECT pg_sleep(1);
select pg_stat_get_db_tuples_inserted(a.oid)>0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_tuples_inserted(a.oid)=0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
drop table sales cascade;
alter system set autovacuum to on;