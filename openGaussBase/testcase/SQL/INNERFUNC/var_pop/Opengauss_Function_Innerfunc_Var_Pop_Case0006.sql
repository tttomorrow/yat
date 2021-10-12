-- @testpoint: 聚集函数var_pop，入参为二进制类型,合理报错

drop table if exists t_nvl_rca_tab;
create table t_nvl_rca_tab(col_1 raw);
insert into t_nvl_rca_tab values (HEXTORAW('DEADBEEF'));
select var_pop(col_1) from t_nvl_rca_tab;
drop table if exists t_nvl_rca_tab;