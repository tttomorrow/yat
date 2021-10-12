-- @testpoint: lengthb函数入参为数值类型
drop table if exists t_nvl_rca_tab;
create table t_nvl_rca_tab(COL_1 bigint);
insert into t_nvl_rca_tab values(12345678);
select distinct LENGTHB(COL_1) from t_nvl_rca_tab;
drop table t_nvl_rca_tab;
