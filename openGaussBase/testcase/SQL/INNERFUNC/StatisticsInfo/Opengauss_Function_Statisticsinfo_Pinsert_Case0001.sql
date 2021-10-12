-- @testpoint: pg_stat_get_partition_tuples_inserted(oid)获取插入相应分区表中行的数量。
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
( PARTITION p1 VALUES LESS THAN ('2019-02-01 00:00:00'),
  PARTITION p2 VALUES LESS THAN ('2019-02-02 00:00:00')
);
select pg_stat_get_partition_tuples_inserted(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_tuples_inserted(a.oid) from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
-- 数据插入分区p1    1 0
INSERT INTO sales VALUES(1, 12, '2019-01-10 00:00:00', 'a', 1, 1, 1);
SELECT pg_sleep(1);
select pg_stat_get_partition_tuples_inserted(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_tuples_inserted(a.oid) from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
-- 数据插入分区p2      1 1
INSERT INTO sales VALUES(1, 12, '2019-02-01 00:00:00', 'a', 1, 1, 1);
SELECT pg_sleep(1);
select pg_stat_get_partition_tuples_inserted(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_tuples_inserted(a.oid) from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
-- 新分区的范围为 '2019-02-05 00:00:00' <= time_id < '2019-02-06 00:00:00'
INSERT INTO sales VALUES(1, 12, '2019-02-05 00:00:00', 'a', 1, 1, 1);
-- 新分区的范围为 '2019-02-03 00:00:00' <= time_id < '2019-02-04 00:00:00'
INSERT INTO sales VALUES(1, 12, '2019-02-03 00:00:00', 'a', 1, 1, 1);
-- 查看分区信息  1 1 1 1
SELECT pg_sleep(1);
select pg_stat_get_partition_tuples_inserted(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_tuples_inserted(a.oid) from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_tuples_inserted(a.oid) from pg_partition  a, pg_class b where a.relname = 'sys_p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_tuples_inserted(a.oid) from pg_partition  a, pg_class b where a.relname = 'sys_p2' and b.oid=a.parentid and b.relname='sales';
-- 删除数据  不会变化，记录的是insert的次数
delete  from  sales  where channel_id = 'a';
SELECT pg_sleep(1);
select pg_stat_get_partition_tuples_inserted(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_tuples_inserted(a.oid) from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_tuples_inserted(a.oid) from pg_partition  a, pg_class b where a.relname = 'sys_p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_tuples_inserted(a.oid) from pg_partition  a, pg_class b where a.relname = 'sys_p2' and b.oid=a.parentid and b.relname='sales';
drop table sales cascade;
alter system set autovacuum to on;