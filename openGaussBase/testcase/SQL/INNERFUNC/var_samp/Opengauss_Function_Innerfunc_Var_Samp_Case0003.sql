-- @testpoint: 聚集函数var_samp，入参为''/null

drop table if exists t_nvl_rca_tab;
create table t_nvl_rca_tab(col_1 int);
insert into t_nvl_rca_tab values ('');
insert into t_nvl_rca_tab values (null);
insert into t_nvl_rca_tab values (null);
select var_samp(col_1) from t_nvl_rca_tab;
drop table if exists t_nvl_rca_tab;