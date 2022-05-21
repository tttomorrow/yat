-- @testpoint: pg_stat_get_tuples_deleted(oid)函数的异常校验，合理报错
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
-- 数据插入
INSERT INTO sales VALUES(1, 12, '2017-01-10 00:00:00', 'a', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-05-01 10:00:00', 'b', 1, 1, 1);
-- 更新数据
delete  from  sales  where channel_id = 'a';
select pg_stat_get_tuples_deleted() from PG_CLASS a where a.relname = 'sales';
delete  from  sales  where channel_id = 'b';
select pg_stat_get_tuples_deleted(a.oid,a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_tuples_deleted(98887787708976687654) from PG_PARTITION a where a.relname = 'p2';
drop table sales cascade;