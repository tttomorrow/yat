-- @testpoint: 字符处理函数，入参为时间类型（date,timestamp）类型

drop table if exists t_nvl_rca_tab;
create table t_nvl_rca_tab(col_1 date,col_2 time,col_3 timestamp,col_4 smalldatetime,col_5 reltime);
insert into t_nvl_rca_tab (col_1,col_2,col_3,col_4,col_5)values ('12-10-2010','21:21:21','2010-12-12','2003-04-12 04:05:06','P-1.1Y10M');
select upper(col_1),upper(col_2),upper(col_3),upper(col_4),upper(col_5) from t_nvl_rca_tab;
drop table if exists t_nvl_rca_tab;