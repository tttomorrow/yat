-- @testpoint: pg_stat_get_dead_tuples(oid)返回表的死行数
--记录的是更新和删除的行数
alter system set autovacuum to off;
SELECT pg_sleep(6);
SELECT pg_sleep(6);
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
-- 无数据查询
select pg_stat_get_dead_tuples(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 数据插入sales
INSERT INTO sales VALUES(1, 12, '2019-01-10 00:00:00', 'a', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-01 00:00:00', 'b', 1, 1, 1);
select pg_stat_get_dead_tuples(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 更新一行数据,旧的其实还在，只是指针指向了新数据，因此dead记录1
update sales set time_id = '2019-06-02 10:00:00' where channel_id = 'b';
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_dead_tuples(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 再添加数据 1
INSERT INTO sales VALUES(1, 12, '2019-02-05 00:00:00', 'c', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-03 00:00:00', 'd', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-05 00:00:00', 'e', 1, 1, 1);
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_dead_tuples(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 更新多行 4
update sales set time_id = '2015-06-02 10:00:00' where channel_id = 'c';
update sales set time_id = '2013-06-02 10:00:00' where channel_id = 'd';
update sales set time_id = '2012-06-02 10:00:00' where channel_id = 'e';
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_dead_tuples(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 删除一行 5
delete from sales where channel_id = 'b';
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_dead_tuples(a.oid) from PG_CLASS a where a.relname = 'sales';
-- 删除多行 8
delete from sales where channel_id = 'c';
delete from sales where channel_id = 'd';
delete from sales where channel_id = 'e';
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_dead_tuples(a.oid) from PG_CLASS a where a.relname = 'sales';
drop table sales cascade;
alter system set autovacuum to on; 