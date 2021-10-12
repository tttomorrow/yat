-- @testpoint: pg_stat_get_tuples_changed(oid)函数的异常校验，合理报错
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
);
-- 未插入数据未analyse 0
select pg_stat_get_tuples_changed() from PG_CLASS a where a.relname = 'sales';
-- 未插入数据先analyse 0
ANALYZE sales;
select pg_stat_get_tuples_changed(a.oid,a.oid) from PG_CLASS a where a.relname = 'sales';
-- analyse 后插入数据 1
INSERT INTO sales VALUES(1, 12, '2019-01-10 00:00:00', 'a', 1, 1, 1);
-- analyse 后删除一行
delete  from  sales  where channel_id = 'a';
select pg_stat_get_tuples_changed('’*&^#$%^&*‘') from PG_CLASS a where a.relname = 'sales';
drop table sales cascade;