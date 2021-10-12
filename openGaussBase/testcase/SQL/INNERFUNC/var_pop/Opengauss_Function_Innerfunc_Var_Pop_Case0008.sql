-- @testpoint: 聚集函数var_pop,入参为算数表达式
drop table if exists t_nvl_rca_tab;
create table t_nvl_rca_tab(col_1 int);
insert into t_nvl_rca_tab values (253);
insert into t_nvl_rca_tab values (254);
insert into t_nvl_rca_tab values (255);
select var_pop((col_1+10)/3) from t_nvl_rca_tab;
drop table if exists t_nvl_rca_tab;