-- @testpoint: pg_stat_get_db_blocks_fetched(oid)返回数据库中磁盘块抓取请求的总数。
-- 先清理环境
alter system set autovacuum to off;
drop table if exists sales;
select pg_stat_reset();
--创建表sales
CREATE TABLE sales
(prod_id numeric(6),
 cust_id numeric,
 time_id DATE,
 channel_id CHAR(1),
 promo_id numeric(6),
 quantity_sold numeric(3),
 amount_sold numeric(10,2)
);
-- testpoint2:创建索引
create index test_index1 on sales (channel_id);
SELECT pg_sleep(1);
select pg_stat_get_db_blocks_fetched(a.oid) > 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_blocks_fetched(a.oid) = 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- testpoint3:插入一行数据的磁盘获取数
select pg_stat_reset();
declare
begin
    for i in 1..10000 loop
        INSERT INTO sales VALUES(i, 12, '2018-01-10 00:00:00', 'a', 1, 1, 1);
    end loop;
end;
/
SELECT pg_sleep(1);
select pg_stat_get_db_blocks_fetched(a.oid) > 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_blocks_fetched(a.oid) = 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- testpoint4: 验证更新数据的磁盘获取数
select pg_stat_reset();
-- 更新多行
declare
begin
    for i in 1..10 loop
        update sales set amount_sold = i where channel_id = 'a';
    end loop;
end;
/
SELECT pg_sleep(1);
select pg_stat_get_db_blocks_fetched(a.oid) > 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_blocks_fetched(a.oid) = 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- testpoint5:验证删除数据的磁盘获取数
select pg_stat_reset();
-- 删除多行
delete from sales where channel_id = 'a';
SELECT pg_sleep(2);
select pg_stat_get_db_blocks_fetched(a.oid) > 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_blocks_fetched(a.oid) = 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- testpoint6: 查表请求
select * from sales;
SELECT pg_sleep(1);
select pg_stat_get_db_blocks_fetched(a.oid) > 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_blocks_fetched(a.oid) = 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- 恢复环境
drop table sales cascade;
alter system set autovacuum to on;