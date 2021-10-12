-- @testpoint: 字符处理函数，入参为二进制类型,合理报错

drop table if exists t_nvl_rca_tab;
create table t_nvl_rca_tab(col_1 raw, col_4 bytea);
insert into t_nvl_rca_tab values (HEXTORAW('DEADBEEF'),E'\\xDEADBEEF');
select upper(col_1),upper(col_4) from t_nvl_rca_tab;
drop table t_nvl_rca_tab;