-- @testpoint: pg_stat_get_tuples_hot_updated(oid)函数的异常校验，合理报错
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
-- 未插入数据，在创建索引前后查
select pg_stat_get_tuples_hot_updated() from PG_CLASS a where a.relname = 'sales';
-- 数据插入sales
INSERT INTO sales VALUES(1, 12, '2019-01-10 00:00:00', 'a', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-01 00:00:00', 'b', 1, 1, 1);
create index test_index on sales(prod_id);
select pg_stat_get_tuples_hot_updated(a.oid,a.oid,a.oid) from PG_CLASS a where a.relname = 'sales';
-- 更新一条
update sales set time_id = '2017-12-10 00:00:00' where channel_id = 'a';
select pg_stat_get_tuples_hot_updated(’87654345888765#￥%……&*‘) from PG_CLASS a where a.relname = 'sales';
-- 一条更新多次
update sales set time_id = '2019-06-02 10:00:00' where channel_id = 'b';
update sales set time_id = '2019-06-03 10:00:00' where channel_id = 'b';
select pg_stat_get_tuples_hot_updated(987653456789987654);
drop table sales cascade;
