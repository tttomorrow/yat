-- @testpoint: pg_stat_get_backend_userid(integer),当入参为无效值（为空、字母、特殊字符、多参）时，合理报错

select pg_stat_get_backend_userid();
select pg_stat_get_backend_userid('abc');
select pg_stat_get_backend_userid('@#%');
select pg_stat_get_backend_userid(1,2);