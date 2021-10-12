-- @testpoint: 聚集函数var_pop,入参为汉字及特殊字符，合理报错
drop table if exists t_nvl_rca_tab;
create table t_nvl_rca_tab(col_1 varchar,col_2 varchar);
insert into t_nvl_rca_tab values ('你好','&……%');
insert into t_nvl_rca_tab values ('我好','+_*');
select var_pop(col_1) from t_nvl_rca_tab;
select var_pop(col_2) from t_nvl_rca_tab;
drop table if exists t_nvl_rca_tab;