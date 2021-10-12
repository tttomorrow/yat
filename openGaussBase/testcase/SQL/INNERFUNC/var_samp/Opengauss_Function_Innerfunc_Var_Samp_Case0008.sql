-- @testpoint: 聚集函数var_samp，与group by、having联合使用
drop table if exists t_nvl_rca_tab;
create table t_nvl_rca_tab(col_1 int,col_2 int);
insert into t_nvl_rca_tab values (253,333);
insert into t_nvl_rca_tab values (254,111);
insert into t_nvl_rca_tab values (255,987);
select distinct var_samp(col_2),grouping(col_1) from t_nvl_rca_tab group by cube(col_1,col_2) having var_samp(abs(-col_1*-col_2))>100 and var_samp(col_2)>1 order by 1,2;
drop table if exists t_nvl_rca_tab;