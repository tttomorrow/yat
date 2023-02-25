-- @testpoint: cast用例,部分用例合理报错
-- as用逗号代替
--新建表
create table t_Opengauss_CAST_Case0043_1(a int,c money,b timestamp);
-- as用逗号代替
select cast(c , unsigned) from t_Opengauss_CAST_Case0043_1;
select cast(b , unsigned) from t_Opengauss_CAST_Case0043_1;
select cast(a , unsigned) from t_Opengauss_CAST_Case0043_1;
-- 清理环境
drop table t_Opengauss_CAST_Case0043_1;
