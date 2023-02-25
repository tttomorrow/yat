-- @testpoint: cast用例,部分用例合理报错
--转换存在表的多个字段
--新建表
create table t_Opengauss_CAST_Case0039_1(a int,c money,b timestamp);
--转换存在表的多个字段
select cast(a,c as unsigned) from t_Opengauss_CAST_Case0039_1;
select cast(a c as unsigned) from t_Opengauss_CAST_Case0039_1;
select cast(c,b as unsigned) from t_Opengauss_CAST_Case0039_1;
select cast(c b as unsigned) from t_Opengauss_CAST_Case0039_1;
--清理环境
drop table t_Opengauss_CAST_Case0039_1;
