-- @testpoint: pg_stat_get_partition_tuples_changed(oid)函数的异常校验，合理报错
alter system set autovacuum to off;
-- 清理环境
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
( PARTITION p1 VALUES LESS THAN ('3000-01-01 00:00:00'),
  PARTITION p2 VALUES LESS THAN ('4000-12-31 00:00:00')
);
analyze sales;
INSERT INTO sales VALUES(2, 12, '2018-01-10 00:00:00', 'a', 1, 1, 1);
update sales set time_id = '2019-06-02 10:00:00' where channel_id = 'a';
delete from sales where channel_id = 'a';
SELECT pg_sleep(1);
--  testpoint:空值、多参、少参、oid错误
select pg_stat_get_partition_tuples_changed('') from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_tuples_changed(a.oid,a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_tuples_changed() from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_tuples_changed('*&^%') from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_tuples_changed(999999) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
drop table if exists sales;
alter system set autovacuum to on;