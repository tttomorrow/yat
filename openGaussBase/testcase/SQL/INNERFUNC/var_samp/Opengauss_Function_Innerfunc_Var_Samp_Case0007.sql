-- @testpoint: 聚集函数var_samp，入参为时间类型（date,timestamp）类型，合理报错

drop table if exists t_nvl_rca_tab;
create table t_nvl_rca_tab(col_1 date,col_2 time,col_3 timestamp,col_4 smalldatetime);
insert into t_nvl_rca_tab values ('12-10-2010','21:21:21','2010-12-12','2003-04-12 04:05:06');
insert into t_nvl_rca_tab values ('12-10-2023','21:21:21','2010-12-12','2003-04-12 04:05:06');
select var_samp(col_1) from t_nvl_rca_tab;
drop table if exists t_nvl_rca_tab;
