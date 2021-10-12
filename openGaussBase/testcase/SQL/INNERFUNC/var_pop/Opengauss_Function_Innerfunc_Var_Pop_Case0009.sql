-- @testpoint: 聚集函数var_pop，与其它函数嵌套使用
drop table if exists t_nvl_rca_tab;
create table t_nvl_rca_tab(col_1 float);
insert into t_nvl_rca_tab values (253.1);
insert into t_nvl_rca_tab values (-254);
insert into t_nvl_rca_tab values (255.9);
select var_pop(ceil(abs(col_1))) from t_nvl_rca_tab;
drop table if exists t_nvl_rca_tab;