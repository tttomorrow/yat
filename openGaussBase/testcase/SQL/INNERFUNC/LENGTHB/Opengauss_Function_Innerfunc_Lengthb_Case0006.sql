-- @testpoint: lengthb函数入参为时间类型（date,TIMESTAMP）类型
drop table if exists t_nvl_rca_tab;
create table t_nvl_rca_tab( 
COL_1 DATE,COL_2 TIMESTAMP);
 INSERT INTO t_nvl_rca_tab VALUES (date '12-10-2010','2013-12-11 pst');
select distinct LENGTHB(COL_1),LENGTHB(COL_2) from t_nvl_rca_tab;
drop table t_nvl_rca_tab;