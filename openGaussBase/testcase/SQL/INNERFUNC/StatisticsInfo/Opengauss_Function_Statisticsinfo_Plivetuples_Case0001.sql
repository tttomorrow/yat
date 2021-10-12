-- @testpoint: pg_stat_get_partition_live_tuples(oid)查询分区表里的活行数。
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
)
PARTITION BY RANGE (time_id)
INTERVAL('1 day')
( PARTITION p1 VALUES LESS THAN ('2019-01-01 00:00:00'),
  PARTITION p2 VALUES LESS THAN ('2019-12-31 00:00:00')
);
-- 无数据查询
select pg_stat_get_partition_live_tuples(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_live_tuples(a.oid) from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
-- 数据插入sales 1 0
INSERT INTO sales VALUES(1, 12, '2018-01-10 00:00:00', 'a', 1, 1, 1);
SELECT pg_sleep(2);
select pg_stat_get_partition_live_tuples(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_live_tuples(a.oid) from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
-- 再添加数据 2 2
INSERT INTO sales VALUES(1, 12, '2018-02-01 00:00:00', 'b', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-05 00:00:00', 'c', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-08-03 00:00:00', 'd', 1, 1, 1);
SELECT pg_sleep(2);
select pg_stat_get_partition_live_tuples(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_live_tuples(a.oid) from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
-- 更新数据 1 3
update sales set time_id = '2019-06-02 10:00:00' where channel_id = 'b';
SELECT pg_sleep(2);
select pg_stat_get_partition_live_tuples(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_live_tuples(a.oid) from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
-- 删除数据  0 1
delete from sales where channel_id = 'a';
delete from sales where channel_id = 'b';
delete from sales where channel_id = 'c';
SELECT pg_sleep(2);
select pg_stat_get_partition_live_tuples(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_live_tuples(a.oid) from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
drop table sales cascade;
alter system set autovacuum to on;