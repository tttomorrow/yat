-- @testpoint: pg_stat_get_bgwriter_timed_checkpoints()描述：后台写进程开启定时检查点的时间

select pg_stat_get_bgwriter_timed_checkpoints();