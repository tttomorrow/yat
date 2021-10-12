-- @testpoint: pg_stat_get_backend_start(integer) 给定服务器进程启动的时间，入参为为空、字母、特殊字符时，合理报错

select pg_stat_get_backend_start();
select pg_stat_get_backend_start('a');
select pg_stat_get_backend_start('@#$');