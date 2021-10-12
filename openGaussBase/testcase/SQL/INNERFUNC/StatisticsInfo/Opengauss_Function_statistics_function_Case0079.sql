-- @testpoint: 函数pg_stat_get_backend_pid(integer)，给定的服务器线程的线程ID，入参为无效值（空、字母、特殊字符时、多参）时，合理报错

select pg_stat_get_backend_pid();
select pg_stat_get_backend_pid('a');
select pg_stat_get_backend_pid('_@&');
select pg_stat_get_backend_pid(1,2);