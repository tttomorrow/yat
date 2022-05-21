-- @testpoint: pg_stat_get_db_xact_commit(oid)返回数据库中已提交事务的数量。
alter system set autovacuum to off;
drop table if exists test;
CREATE TABLE test
 (
     sk            INTEGER               NOT NULL,
     id            CHAR(16)              NOT NULL,
     name          VARCHAR(20)                   ,
     grade              DECIMAL(5,2)
 );
-- testpoint:begin end、增删改等都会是一次事务提交
begin;
/
select * from test;
end;
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_db_xact_commit(a.oid) >0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_xact_commit(a.oid) =0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- 增
select pg_stat_reset();
insert into test values (1,'a','sing',90.9);
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_db_xact_commit(a.oid) >0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_xact_commit(a.oid) =0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- 改
select pg_stat_reset();
update test set grade = 99.99 where sk = 1;
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_db_xact_commit(a.oid)>0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_xact_commit(a.oid) =0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- 删
select pg_stat_reset();
delete from test where sk = 1;
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_db_xact_commit(a.oid) >0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_xact_commit(a.oid) =0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- 清理环境
drop table test;
alter system set autovacuum to on;