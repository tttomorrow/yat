-- @testpoint: 聚集函数var_pop，入参为字符串，合理报错

drop table if exists t_nvl_rca_tab;
create table t_nvl_rca_tab(col_1 varchar);
insert into t_nvl_rca_tab values ('sqlll');
insert into t_nvl_rca_tab values ('pythonnnn');
select var_pop(col_1) from t_nvl_rca_tab;
drop table if exists t_nvl_rca_tab;