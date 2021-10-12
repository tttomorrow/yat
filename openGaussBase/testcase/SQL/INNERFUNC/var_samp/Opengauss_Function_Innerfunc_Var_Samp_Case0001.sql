-- @testpoint: 聚集函数var_samp，入参为浮点数

drop table if exists t_nvl_rca_tab;
create table t_nvl_rca_tab(col_1 NUMERIC(10,4));
insert into t_nvl_rca_tab values(123456.123);
insert into t_nvl_rca_tab values(123454.12354);
select var_samp(col_1) from t_nvl_rca_tab;
drop table if exists t_nvl_rca_tab;
