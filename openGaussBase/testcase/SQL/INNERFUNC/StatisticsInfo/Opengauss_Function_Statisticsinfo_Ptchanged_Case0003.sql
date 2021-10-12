-- @testpoint: pg_stat_get_partition_tuples_changed(oid)对autoanalyze之后插入、更新、删除行的总数量获取。
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
SELECT pg_sleep(1);
select pg_stat_get_partition_tuples_changed(a.oid)  from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
SELECT pg_sleep(1);
select pg_stat_get_partition_tuples_changed(a.oid)  from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
-- 插入多于50行数据触发自动分析
declare
begin
    for i in 1..10000 loop
        INSERT INTO sales VALUES(i, 12, '2018-01-10 00:00:00', 'a', 1, 1, 1);
    end loop;
end;
/
select count(*) from sales;
SELECT pg_sleep(1);
select pg_stat_get_partition_tuples_changed(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
-- 更新、删除数据
update sales set time_id = '2019-06-02 10:00:00' where channel_id = 'a';
delete from sales where channel_id = 'a';
SELECT pg_sleep(1);
select pg_stat_get_partition_tuples_changed(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_partition_tuples_changed(a.oid) from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
drop table sales cascade;
alter system set autovacuum to on;