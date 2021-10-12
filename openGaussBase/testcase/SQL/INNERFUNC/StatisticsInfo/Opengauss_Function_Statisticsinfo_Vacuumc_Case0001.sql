-- @testpoint: pg_stat_get_vacuum_count(oid)返回用户在某表上手动启动清理的次数。
alter system set autovacuum to off;
-- 清理环境
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
declare
begin
    for i in 1..10000 loop
        INSERT INTO sales VALUES(i, 12, '2018-01-10 00:00:00', 'a', 1, 1, 1);
    end loop;
end;
/
-- testpoint：无死行查询是0
select pg_stat_get_vacuum_count(a.oid) = 0 from pg_class  a where a.relname = 'sales';
-- testpoint：更新数据后旧的行还存在，进行清理
update sales set time_id = '2019-06-02 10:00:00' where channel_id = 'a';
vacuum sales;
SELECT pg_sleep(10);
select pg_stat_get_vacuum_count(a.oid)  from pg_class  a where a.relname = 'sales';
-- testpoint：删除数据后进行清理
delete from sales where channel_id = 'a';
vacuum sales;
SELECT pg_sleep(10);
select pg_stat_get_vacuum_count(a.oid)  from pg_class  a where a.relname = 'sales';
vacuum sales;
SELECT pg_sleep(10);
select pg_stat_get_vacuum_count(a.oid)  from pg_class  a where a.relname = 'sales';
drop table sales cascade;
alter system set autovacuum to on;