-- @testpoint: pg_stat_get_db_conflict_lock(oid)，数据库中死锁的数量，入参为无效值时，合理报错

----step1：入参为空; expect:合理报错
select pg_stat_get_db_conflict_lock() from PG_DATABASE a where a.datname = datname;

----step2：多参; expect:合理报错
select pg_stat_get_db_conflict_lock(a.oid,a.oid,a.oid) from PG_DATABASE a where a.datname = datname;

----step3：入参超范围; expect:合理报错
select pg_stat_get_db_conflict_lock(9999999999999) from PG_DATABASE a where a.datname = datname;

----step4：入参为特殊字符; expect:合理报错
select pg_stat_get_db_conflict_lock('*&^%$') from PG_DATABASE a where a.datname = datname;