-- @testpoint: pg_stat_get_backend_dbid(integer)，给定服务器进程的数据库ID, 入参为有效值时

select pg_stat_get_backend_dbid(1);