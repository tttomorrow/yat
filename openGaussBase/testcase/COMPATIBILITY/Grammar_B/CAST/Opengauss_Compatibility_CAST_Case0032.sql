-- @testpoint: cast用例,部分用例合理报错
-- 新建模式
create schema sch_Opengauss_CAST_Case0032_1;
-- 跨模式进行类型转换
select sch_Opengauss_CAST_Case0032_1.cast(cast('$2'::money as unsigned) as money);
-- 清理环境
drop schema sch_Opengauss_CAST_Case0032_1;;
