-- @testpoint: pg_stat_get_role_name(oid)函数的异常校验，合理报错

-- testpoint：oid错误、多参、少参、空值
-- 开发确认oid不存在时返回结果是空字符串
select char_length(pg_stat_get_role_name(00000))=0;
select pg_stat_get_role_name(9999999999999);
DROP USER if exists kim cascade;
CREATE USER kim IDENTIFIED BY 'Bigdata@123';
select pg_stat_get_role_name(a.oid,a.oid,a.oid) from PG_ROLES a where a.rolname = 'kim';
select pg_stat_get_role_name() from PG_ROLES a where a.rolname = 'kim';
select pg_stat_get_role_name('') from PG_ROLES a where a.rolname = 'kim';
DROP USER kim CASCADE;
