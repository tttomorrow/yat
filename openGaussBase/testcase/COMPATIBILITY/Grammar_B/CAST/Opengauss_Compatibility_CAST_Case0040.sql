-- @testpoint: cast用例,部分用例合理报错
-- 转换存在表的某个存在字段
--新建表
create table t_Opengauss_CAST_Case0040_1(a int,c money,b timestamp);
--插入数据
-- 转换存在表的某个存在字段
select cast(c as unsigned) from t_Opengauss_CAST_Case0040_1;
select cast(b as unsigned) from t_Opengauss_CAST_Case0040_1;
select cast(a as unsigned) from t_Opengauss_CAST_Case0040_1;
-- 清理环境
drop table t_Opengauss_CAST_Case0040_1;
