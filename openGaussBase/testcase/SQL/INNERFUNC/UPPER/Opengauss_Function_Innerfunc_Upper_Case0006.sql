-- @testpoint: 字符处理函数upper,入参为clob类型

drop table if exists t_nvl_rca_tab;
create table t_nvl_rca_tab(col_1 clob, col_4 clob);
insert into t_nvl_rca_tab values ('我是java','我是python');
select upper(col_1),upper(col_4) from t_nvl_rca_tab;
drop table if exists t_nvl_rca_tab;