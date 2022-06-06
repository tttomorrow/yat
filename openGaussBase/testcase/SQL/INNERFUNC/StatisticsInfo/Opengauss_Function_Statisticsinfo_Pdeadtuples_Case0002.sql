-- @testpoint: pg_stat_get_partition_dead_tuples(oid)函数的异常校验，合理报错
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
-- 数据插入sales
INSERT INTO sales VALUES(1, 12, '2018-02-01 00:00:00', 'b', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-05 00:00:00', 'c', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-08-03 00:00:00', 'd', 1, 1, 1);
-- 更新数据
update sales set time_id = '2019-06-02 10:00:00' where channel_id = 'b';
update sales set time_id = '2020-06-02 10:00:00' where channel_id = 'd';
select pg_stat_get_partition_dead_tuples() from pg_partition  a where a.relname = 'p1';
select pg_stat_get_partition_dead_tuples(9999999999999999999999999) from pg_partition  a where a.relname = 'p2';
-- 删除数据
delete from sales where channel_id = 'b';
delete from sales where channel_id = 'c';
select pg_stat_get_partition_dead_tuples(a.oid,a.oid,a.oid) from pg_partition  a where a.relname = 'p1';
select pg_stat_get_partition_dead_tuples('*&^%#$') from pg_partition  a where a.relname = 'p2';
drop table sales cascade;