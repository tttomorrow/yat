-- @testpoint: 关键字limit作为全局临时表的列名
drop table if exists t_global_temporary_limit_001;
create global temporary table t_global_temporary_limit_001("limit" int);
--清理环境
drop table if exists t_global_temporary_limit_001;
