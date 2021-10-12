-- @testpoint: pg_stat_get_partition_tuples_inserted(oid)函数的异常校验，合理报错
drop table if exists sales;
--创建表sales
CREATE TABLE sales
(prod_id NUMBER(6),
 time_id DATE
)
PARTITION BY RANGE (time_id)
INTERVAL('1 day')
( PARTITION p1 VALUES LESS THAN ('2019-02-01 00:00:00'),
  PARTITION p2 VALUES LESS THAN ('2019-02-02 00:00:00')
);
-- 数据插入分区p1
INSERT INTO sales VALUES(1, '2019-01-10 00:00:00');
select pg_stat_get_partition_tuples_inserted() from PG_PARTITION a where a.relname = 'p1';
select pg_stat_get_partition_tuples_inserted(a.oid,a.oid) from PG_PARTITION a where a.relname = 'p2';
drop table sales cascade;