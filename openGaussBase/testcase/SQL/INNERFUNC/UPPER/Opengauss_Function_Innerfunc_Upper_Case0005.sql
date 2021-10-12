-- @testpoint: 字符处理函数upper，入参为字符类型

drop table if exists t_nvl_rca_tab;
create table t_nvl_rca_tab(col_1 char(5), col_4 varchar, col_8 text);
insert into t_nvl_rca_tab values ('java','python','sql');
select upper(col_1),upper(col_4),upper(col_8) from t_nvl_rca_tab;
drop table if exists t_nvl_rca_tab;
