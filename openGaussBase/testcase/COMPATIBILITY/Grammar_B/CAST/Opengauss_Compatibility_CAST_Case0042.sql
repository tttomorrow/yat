-- @testpoint: cast用例,部分用例合理报错
-- 不输入参数
--新建表
create table t_Opengauss_CAST_Case0042_1(a int,c money,b timestamp);
-- 不输入参数
select cast() from t_Opengauss_CAST_Case0042_1;
select cast() from t_Opengauss_CAST_Case0042_1;
select cast() from t_Opengauss_CAST_Case0042_1;
-- 清理环境
drop table t_Opengauss_CAST_Case0042_1;
