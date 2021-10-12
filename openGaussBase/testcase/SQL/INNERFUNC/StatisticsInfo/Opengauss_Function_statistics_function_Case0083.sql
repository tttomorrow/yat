-- @testpoint: pg_stat_get_backend_userid(integer)，给定服务器进程的用户ID，当入参为无效值时，合理报错

--入参为有效值时
select pg_stat_get_backend_userid(1);

--当入参为无效值（为空、字母、特殊字符、多参）时
select pg_stat_get_backend_userid();
select pg_stat_get_backend_userid('abc');
select pg_stat_get_backend_userid('@#%');
select pg_stat_get_backend_userid(1,2);