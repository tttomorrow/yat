-- @testpoint: 关键字limit作为全局临时表的列名在insert语句,select语句中使用
drop table if exists t_global_temporary_limit_002;
create global temporary table t_global_temporary_limit_002("limit" int) on commit preserve rows;
insert into t_global_temporary_limit_002 values (1);
commit;
select "limit" from t_global_temporary_limit_002 order by "limit";
--清理环境
drop table if exists t_global_temporary_limit_002;