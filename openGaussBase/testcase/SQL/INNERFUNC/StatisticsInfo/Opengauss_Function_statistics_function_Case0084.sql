-- @testpoint: pg_stat_get_bgwriter_requested_checkpoints()描述：后台写进程开启基于后端请求的检查点的时间

select pg_stat_get_bgwriter_requested_checkpoints();
