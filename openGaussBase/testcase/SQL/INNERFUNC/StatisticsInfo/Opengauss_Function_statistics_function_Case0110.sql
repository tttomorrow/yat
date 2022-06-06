-- @testpoint: pg_stat_get_db_cu_hdd_asyn(oid)，入参为无效值时，合理报错

----step1：入参为空; expect:合理报错
select pg_stat_get_db_cu_hdd_asyn() from PG_DATABASE a where a.datname = 'postgres';

----step2：多参; expect:合理报错
select pg_stat_get_db_cu_hdd_asyn(a.oid,a.oid,a.oid) from PG_DATABASE a where a.datname = 'postgres';

----step3：入参超范围; expect:合理报错
select pg_stat_get_db_cu_hdd_asyn(9999999999999) from PG_DATABASE a where a.datname = 'postgres';

----step4：入参为特殊字符; expect:合理报错
select pg_stat_get_db_cu_hdd_asyn('*&^%$') from PG_DATABASE a where a.datname = 'postgres';