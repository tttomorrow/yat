-- @testpoint: cast用例
--新建表
create table t_Opengauss_CAST_Case0041_1(a int,c money,b timestamp);
-- 转换存在表的某个存在字段
select cast(c as unsigned) from t_Opengauss_CAST_Case0041_1;
select cast(b as unsigned) from t_Opengauss_CAST_Case0041_1;
select cast(a as unsigned) from t_Opengauss_CAST_Case0041_1;
-- 转换数据后查看原始数据
select * from t_Opengauss_CAST_Case0041_1;
-- 清理环境
drop table t_Opengauss_CAST_Case0041_1;
