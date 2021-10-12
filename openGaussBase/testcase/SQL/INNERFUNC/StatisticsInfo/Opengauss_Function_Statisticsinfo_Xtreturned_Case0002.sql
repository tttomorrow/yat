-- @testpoint: pg_stat_get_xact_tuples_returned(oid)函数的异常校验，合理报错
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
create index test_index1 on sales (prod_id);
INSERT INTO sales VALUES(1, 12, '2019-02-05 00:00:00', 'c', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-03 00:00:00', 'd', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-05 00:00:00', 'e', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-03 00:00:00', 'f', 1, 1, 1);
select pg_stat_get_xact_tuples_returned() from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_tuples_returned(a.oid,a.oid,a.oid) from PG_CLASS a where a.relname = 'test_index1';
select pg_stat_get_xact_tuples_returned('*&^%$') from PG_CLASS a where a.relname = 'test_index1';
drop table sales cascade;