-- @testpoint: pg_stat_get_xact_tuples_deleted(oid)返回当前事务中表里删除的tuple数
alter system set autovacuum to off;
drop table if exists sales;
begin;
/
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
select pg_stat_get_xact_tuples_deleted(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 数据插入sales 1
INSERT INTO sales VALUES(1, 12, '2019-01-10 00:00:00', 'a', 1, 1, 1);
SELECT pg_sleep(1);
select pg_stat_get_xact_tuples_deleted(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 数据插入sales
INSERT INTO sales VALUES(1, 12, '2019-02-01 00:00:00', 'b', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-05 00:00:00', 'c', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-03 00:00:00', 'd', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-05 00:00:00', 'e', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-03 00:00:00', 'f', 1, 1, 1);
SELECT pg_sleep(1);
select pg_stat_get_xact_tuples_inserted(a.oid) = 6 from PG_CLASS a where a.relname = 'sales';
-- 更新数据 不会影响
update sales set time_id = '2017-12-10 00:00:00' where channel_id = 'a';
SELECT pg_sleep(1);
select pg_stat_get_xact_tuples_deleted(a.oid)  from PG_CLASS a where a.relname = 'sales';
-- 删除数据 1
delete  from  sales  where channel_id = 'e';
SELECT pg_sleep(1);
select pg_stat_get_xact_tuples_deleted(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 删除不存在的数据 1
delete  from  sales  where channel_id = 'e';
SELECT pg_sleep(1);
select pg_stat_get_xact_tuples_deleted(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 删除多行 6
delete  from  sales  where amount_sold = 1;
SELECT pg_sleep(1);
select pg_stat_get_xact_tuples_deleted(a.oid) from PG_CLASS a where a.relname = 'sales';
end;
-- 事务外 0
select pg_stat_get_xact_tuples_deleted(a.oid) = 0 from PG_CLASS a where a.relname = 'sales';
drop table sales cascade;
alter system set autovacuum to on;