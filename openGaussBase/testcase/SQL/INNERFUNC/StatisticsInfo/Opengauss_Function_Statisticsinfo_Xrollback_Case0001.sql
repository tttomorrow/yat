-- @testpoint: pg_stat_get_db_xact_rollback(oid)返回数据库中回滚事务的数量。
--清理环境
alter system set autovacuum to off;
drop table if exists test;
select pg_stat_reset();
CREATE TABLE test
 (
     name          VARCHAR(20)                   ,
     grade              DECIMAL(5,2)
 );
-- testpoint:建表不统计0
SELECT pg_sleep(1);
select pg_stat_get_db_xact_rollback(a.oid) from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- testpoint:commit不统计0
begin;
/
 insert into test values('joe',3);
end;
SELECT pg_sleep(1);
select pg_stat_get_db_xact_rollback(a.oid)  from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- testpoint:rollback计数
begin;
/
insert into test values('joe',4);
ROLLBACK;
SELECT pg_sleep(1);
--查询是1
select pg_stat_get_db_xact_rollback(a.oid)  from PG_DATABASE a where a.datname = CURRENT_CATALOG;
begin;
/
delete from test where grade = 3;
ROLLBACK;
SELECT pg_sleep(1);
--查询是2
select pg_stat_get_db_xact_rollback(a.oid)  from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- 清计数后是0
select pg_stat_reset();
SELECT pg_sleep(1);
select pg_stat_get_db_xact_rollback(a.oid) from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- 恢复环境
drop table if exists test;
alter system set autovacuum to on;