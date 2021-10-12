-- @testpoint: pg_stat_get_backend_dbid(integer) ,给定服务器进程的数据库ID，当入参为无效值（为空、字母、特殊字符、多参）时，合理报错

select pg_stat_get_backend_dbid();
select pg_stat_get_backend_dbid('abc');
select pg_stat_get_backend_dbid('@#%');
select pg_stat_get_backend_dbid(1,2);
