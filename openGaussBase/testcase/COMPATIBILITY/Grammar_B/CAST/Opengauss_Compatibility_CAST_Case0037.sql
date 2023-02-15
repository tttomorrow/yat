-- @testpoint: cast用例,部分用例合理报错
-- 转换不存在表中的某个字段
--新建表
create table t_Opengauss_CAST_Case0037_1(a int,c money,b timestamp);
-- 转换不存在表中的某个字段
select cast(d as unsigned) from t_Opengauss_CAST_Case0037_2;
select cast(e as unsigned) from t_Opengauss_CAST_Case0037_3;
select cast(f as unsigned) from t_Opengauss_CAST_Case0037_4;
-- 清理环境
drop table t_Opengauss_CAST_Case0037_1;
