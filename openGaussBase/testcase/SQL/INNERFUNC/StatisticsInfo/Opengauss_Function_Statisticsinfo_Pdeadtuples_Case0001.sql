-- @testpoint: pg_stat_get_partition_dead_tuples(oid)查询分区表的死行数。
alter system set autovacuum to off;
-- 先清理环境
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
select pg_stat_get_partition_dead_tuples(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_dead_tuples(a.oid) from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
-- 数据插入sales
declare
begin
    for i in 1..10000 loop
        INSERT INTO sales VALUES(i, 12, '2018-01-10 00:00:00', 'a', 1, 1, 1);
		INSERT INTO sales VALUES(i, 12, '2019-11-10 00:00:00', 'b', 1, 1, 1);
    end loop;
end;
/
SELECT pg_sleep(1);
select pg_stat_get_partition_dead_tuples(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_dead_tuples(a.oid) from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
-- 更新数据
update sales set time_id = '2017-06-02 10:00:00' where channel_id = 'a';
SELECT pg_sleep(2);
select pg_stat_get_partition_dead_tuples(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_dead_tuples(a.oid) from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
-- 删除数据
delete from sales where amount_sold = 1;
SELECT pg_sleep(2);
select pg_stat_get_partition_dead_tuples(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_dead_tuples(a.oid) from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
drop table sales cascade;
alter system set autovacuum to on;