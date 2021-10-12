-- @testpoint: 聚集函数var_pop，入参为字符串（数值型）

drop table if exists t_nvl_rca_tab;
create table t_nvl_rca_tab(col_1 varchar);
insert into t_nvl_rca_tab values ('123');
insert into t_nvl_rca_tab values ('456');
select var_pop(col_1) from t_nvl_rca_tab;
drop table if exists t_nvl_rca_tab;

