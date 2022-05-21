-- @testpoint: pg_stat_get_db_numbackends(oid),处理该数据库活跃的服务器进程数目,入参为无效值时，合理报错

----step1：入参为空; expect:合理报错
select pg_stat_get_db_numbackends() from PG_DATABASE a where a.datname = datname;

----step2：多参; expect:合理报错
select pg_stat_get_db_numbackends(a.oid,a.oid,a.oid) from PG_DATABASE a where a.datname = datname;

----step3：入参超范围; expect:合理报错
select pg_stat_get_db_numbackends(9999999999999) from PG_DATABASE a where a.datname = datname;

----step4：入参为特殊字符; expect:合理报错
select pg_stat_get_db_numbackends('*&^%$') from PG_DATABASE a where a.datname = datname;
