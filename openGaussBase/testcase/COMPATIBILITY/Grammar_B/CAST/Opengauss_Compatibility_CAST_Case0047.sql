-- @testpoint: cast用例,部分用例合理报错
-- as前为其他类型的expr
--新建表
create table t_Opengauss_CAST_Case0047_1(a int,c money,b timestamp);
-- 转换存在表的某个存在字段
select cast(select now() as unsigned) from t_Opengauss_CAST_Case0047_1;
select cast(select now() as unsigned) from t_Opengauss_CAST_Case0047_1;
select cast(select current_timestamp as unsigned) from t_Opengauss_CAST_Case0047_1;
-- 清理环境
drop table t_Opengauss_CAST_Case0047_1;
