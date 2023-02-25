-- @testpoint: cast用例,部分用例合理报错
-- as前后有多个type及expr
--新建表
create table t_Opengauss_CAST_Case0045_1(a int,c money,b timestamp);
-- as前后有多个type及expr
select cast(c,b as unsigned) from t_Opengauss_CAST_Case0045_1;
select cast(b c as unsigned) from t_Opengauss_CAST_Case0045_1;
select cast(a as unsigned,timestamp) from t_Opengauss_CAST_Case0045_1;
select cast(a as unsigned timestamp) from t_Opengauss_CAST_Case0045_1;
-- 清理环境
drop table t_Opengauss_CAST_Case0045_1;
