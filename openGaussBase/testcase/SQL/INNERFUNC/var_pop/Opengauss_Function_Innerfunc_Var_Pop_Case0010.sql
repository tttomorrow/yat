-- @testpoint: 聚集函数var_pop,入参为条件表达式
drop table if exists t_nvl_rca_tab;
create table t_nvl_rca_tab(col_1 float,col_2 float);
insert into t_nvl_rca_tab values (253.1,50);
insert into t_nvl_rca_tab values (-254,49);
insert into t_nvl_rca_tab values (255.9,989);
select var_pop(case when COL_2>10 then COL_2 else COL_1 end) from t_nvl_rca_tab;
drop table if exists t_nvl_rca_tab;