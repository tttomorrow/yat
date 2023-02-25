-- @testpoint: cast用例,部分用例合理报错,部分用例合理报错
-- as后为不存在的type
--新建表
create table t_Opengauss_CAST_Case0046_1(a int,c money,b timestamp);
-- 转换存在表的某个存在字段
select cast(c as unsigned1) from t_Opengauss_CAST_Case0046_1;
select cast(b as unsigne) from t_Opengauss_CAST_Case0046_1;
select cast(a as unsign) from t_Opengauss_CAST_Case0046_1;
-- 清理环境
drop table t_Opengauss_CAST_Case0046_1;
