-- @testpoint: 字符处理函数upper，入参为数值类型

drop table if exists t_nvl_rca_tab;
create table t_nvl_rca_tab(col_1 tinyint, col_4 smallint, col_8 integer, col_9 binary_integer, col_10 bigint);
select distinct upper(col_1),upper(col_4),upper(col_8) from t_nvl_rca_tab where upper(col_9)<=upper(col_10) order by 1 limit 10;
drop table if exists t_nvl_rca_tab;
