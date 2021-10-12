-- @testpoint: 关键字limit作为全局临时表的列名在delete语句的使用
drop table if exists t_global_temporary_limit_004;
create global temporary table t_global_temporary_limit_004("limit" int) on commit preserve rows;
insert into t_global_temporary_limit_004 values (1);
commit;
select "limit" from t_global_temporary_limit_004 order by"limit";
delete from t_global_temporary_limit_004 where "limit" = 1;
select "limit" from t_global_temporary_limit_004 order by "limit";
--清理环境
drop table if exists t_global_temporary_limit_004;