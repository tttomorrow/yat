-- @testpoint: pg_stat_get_partition_live_tuples(oid)函数的异常校验，合理报错
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
( PARTITION p1 VALUES LESS THAN ('2019-01-01 00:00:00'),
  PARTITION p2 VALUES LESS THAN ('2019-12-31 00:00:00')
);
select pg_stat_get_partition_live_tuples(a.oid) from pg_class  a where a.relname = 'sales';
select pg_stat_get_partition_live_tuples() from pg_partition  a where a.relname = 'p2';
INSERT INTO sales VALUES(1, 12, '2018-01-10 00:00:00', 'a', 1, 1, 1);
select pg_stat_get_partition_live_tuples(a.oid,a.oid,a.oid) from pg_partition  a where a.relname = 'p1';
select pg_stat_get_partition_live_tuples(9887666989575467897) from pg_partition  a where a.relname = 'p2';
drop table sales cascade;