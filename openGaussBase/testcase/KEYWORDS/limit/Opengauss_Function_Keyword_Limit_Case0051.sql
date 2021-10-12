-- @testpoint: 关键字limit作为全局临时表的列名在update语句的使用
drop table if exists t_global_temporary_limit_003;
create global temporary table t_global_temporary_limit_003("limit" int) on commit preserve rows;
insert into t_global_temporary_limit_003 values (1);
commit;
select "limit" from t_global_temporary_limit_003 order by "limit";
update t_global_temporary_limit_003 set "limit" = 2;
commit;
select"limit" from t_global_temporary_limit_003 order by "limit";
--清理环境
drop table if exists t_global_temporary_limit_003;