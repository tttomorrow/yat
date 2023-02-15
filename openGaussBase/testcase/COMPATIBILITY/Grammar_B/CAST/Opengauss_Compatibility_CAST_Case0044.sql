-- @testpoint: cast用例
-- 新建表
create table t_Opengauss_CAST_Case0044_1(a int,c money,b timestamp);
-- as前为type，as后为expr(0/1,true/false)
select cast(0 as unsigned) from t_Opengauss_CAST_Case0044_1;
select cast(true as unsigned) from t_Opengauss_CAST_Case0044_1;
select cast(1 as unsigned) from t_Opengauss_CAST_Case0044_1;
-- 清理环境
drop table t_Opengauss_CAST_Case0044_1;
