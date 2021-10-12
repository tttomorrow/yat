-- @testpoint: 使用关键字limit为列名的全局临时表创建视图
drop table if exists t_global_temporary_limit_006 cascade;
create global temporary table t_global_temporary_limit_006("limit" int) on commit preserve rows;
insert into t_global_temporary_limit_006 values(1);
commit;
select "limit" from t_global_temporary_limit_006 order by "limit";
create or replace view v_limit_003 as select "limit" from t_global_temporary_limit_006;
select "limit" from v_limit_003;
--清理环境
drop table if exists t_global_temporary_limit_006 cascade;