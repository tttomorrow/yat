-- @testpoint: pg_stat_get_partition_tuples_deleted(oid)查询从相应分区表中删除行的数量。
alter system set autovacuum to off;
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
)
PARTITION BY RANGE (time_id)
INTERVAL('1 day')
( PARTITION p1 VALUES LESS THAN ('2018-01-01 00:00:00'),
  PARTITION p2 VALUES LESS THAN ('2019-12-31 00:00:00')
);
select pg_stat_get_partition_tuples_deleted(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_tuples_deleted(a.oid) from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
-- 数据插入分区p1、p2
INSERT INTO sales VALUES(1, 12, '2017-01-10 00:00:00', 'a', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-05-01 10:00:00', 'b', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-05-01 10:00:00', 'c', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-05-01 10:00:00', 'd', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-05-01 10:00:00', 'e', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-05-01 10:00:00', 'f', 1, 1, 1);
select pg_stat_get_partition_tuples_deleted(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_tuples_deleted(a.oid) from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
-- 删除一行
delete  from  sales  where channel_id = 'a';
SELECT pg_sleep(1);
select pg_stat_get_partition_tuples_deleted(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
-- 删除两行
delete  from  sales  where channel_id = 'b';
delete  from  sales  where channel_id = 'c';
SELECT pg_sleep(1);
select pg_stat_get_partition_tuples_deleted(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_tuples_deleted(a.oid) from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
-- 删除多行
delete  from  sales  where channel_id = 'd';
delete  from  sales  where channel_id = 'e';
delete  from  sales  where channel_id = 'f';
SELECT pg_sleep(1);
select pg_stat_get_partition_tuples_deleted(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_tuples_deleted(a.oid) from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
drop table sales cascade;
alter system set autovacuum to on;