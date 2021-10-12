-- @testpoint: lengthb函数入参为二进制类型
drop table if exists t_nvl_rca_tab;
create table t_nvl_rca_tab( 
COL_1 RAW);
insert into t_nvl_rca_tab values(HEXTORAW('DEADBEEF'));
select distinct LENGTHB(COL_1) from t_nvl_rca_tab;
drop table t_nvl_rca_tab;