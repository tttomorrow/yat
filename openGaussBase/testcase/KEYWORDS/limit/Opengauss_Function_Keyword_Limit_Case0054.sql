-- @testpoint: 在全局临时表关键字limit作为列名的字段上创建索引
drop table if exists t_global_temporary_limit_007;
create global temporary table t_global_temporary_limit_007("limit" int);
create index index_limit_003 on t_global_temporary_limit_007("limit");
select "limit" from t_global_temporary_limit_007;
--清理环境
drop table if exists t_global_temporary_limit_007;
