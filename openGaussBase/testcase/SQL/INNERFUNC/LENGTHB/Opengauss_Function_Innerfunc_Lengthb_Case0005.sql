-- @testpoint: lengthb函数 入参为bool类型，合理报错
drop table if exists t_nvl_rca_tab;
create table t_nvl_rca_tab( 
COL_1 BOOLEAN);
insert into t_nvl_rca_tab values(true);
select distinct LENGTHB(COL_1) from t_nvl_rca_tab;
drop table t_nvl_rca_tab;