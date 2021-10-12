-- @testpoint: pg_stat_get_analyze_count(oid)返回对分区表、普通表手动启动分析后的次数
-- 清理环境
alter system set autovacuum to off;
drop table if exists sales;
drop table if exists t1;
select pg_stat_reset();
--创建表
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
create table t1(id int);
-- analyze 前查询无，返回0
select pg_stat_get_analyze_count(a.oid) from pg_class  a where a.relname = 't1';
select pg_stat_get_analyze_count(a.oid) from pg_class  a where a.relname = 'sales';
select pg_stat_get_analyze_count(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_analyze_count(a.oid) from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
declare
begin
    for i in 1..10000 loop
        INSERT INTO sales VALUES(i, 12, '2018-01-10 00:00:00', 'a', 1, 1, 1);
    end loop;
end;
/
-- analyze
analyze t1;
analyze sales;
analyze sales;
analyze sales partition(p1);
analyze sales partition(p2);
SELECT pg_sleep(1);
select pg_stat_get_analyze_count(a.oid) from pg_class  a where a.relname = 't1';
select pg_stat_get_analyze_count(a.oid) from pg_class  a where a.relname = 'sales';
-- 普通分区表目前支持针对某个分区的统计信息的语法，但功能上不支持针对某个分区的统计信息收集。
select pg_stat_get_analyze_count(a.oid) from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_analyze_count(a.oid) from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
drop table sales cascade;
drop table t1 cascade;
alter system set autovacuum to on;