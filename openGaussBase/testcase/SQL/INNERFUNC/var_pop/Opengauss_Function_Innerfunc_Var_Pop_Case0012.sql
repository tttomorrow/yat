-- @testpoint: 聚集函数var_pop，与case when联合使用
drop table if exists t_nvl_rca_tab;
create table t_nvl_rca_tab(col_1 int,col_2 int);
insert into t_nvl_rca_tab values (253,333);
insert into t_nvl_rca_tab values (254,111);
insert into t_nvl_rca_tab values (255,987);
select case when var_pop(col_1)>var_pop(col_2) then var_pop(col_1) else var_pop(col_2) end from t_nvl_rca_tab;
drop table if exists t_nvl_rca_tab;