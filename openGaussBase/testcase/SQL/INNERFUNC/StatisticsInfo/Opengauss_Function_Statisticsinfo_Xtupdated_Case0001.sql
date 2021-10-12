-- @testpoint: pg_stat_get_xact_tuples_updated(oid)返回当前事务中表更新及热更新的行数
alter system set autovacuum to off;
SELECT pg_sleep(1);
begin;
/
drop table if exists sales;
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
select pg_stat_get_xact_tuples_updated(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 数据插入sales
INSERT INTO sales VALUES(1, 12, '2019-01-10 00:00:00', 'a', 1, 1, 1);
select pg_stat_get_xact_tuples_updated(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 数据插入sales
INSERT INTO sales VALUES(1, 12, '2019-02-01 00:00:00', 'b', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-05 00:00:00', 'c', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-03 00:00:00', 'd', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-05 00:00:00', 'e', 1, 1, 1);
-- 更新一条 1
update sales set time_id = '2017-12-10 00:00:00' where channel_id = 'a';
SELECT pg_sleep(1);
select pg_stat_get_xact_tuples_updated(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 一条更新多次 3，与热更新不同，热更新对相同的update记录一次，这里记录两次
update sales set time_id = '2019-06-02 10:00:00' where channel_id = 'b';
update sales set time_id = '2019-06-02 10:00:00' where channel_id = 'b';
SELECT pg_sleep(1);
select pg_stat_get_xact_tuples_updated(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 更新多条 6
update sales set time_id = '2019-06-01 10:00:00' where channel_id = 'c';
update sales set time_id = '2019-06-02 10:00:00' where channel_id = 'd';
update sales set time_id = '2019-06-03 10:00:00' where channel_id = 'e';
SELECT pg_sleep(1);
select pg_stat_get_xact_tuples_updated(a.oid) from PG_CLASS a where a.relname = 'sales';
end;
-- 事务外自动清0了
select pg_stat_get_xact_tuples_hot_updated(a.oid) from PG_CLASS a where a.relname = 'sales';
drop table sales cascade;
alter system set autovacuum to on;