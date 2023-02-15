-- @testpoint: cast用例,部分用例合理报错,部分用例合理报错
-- cast函数输入参数，as前为expr，后为自定义type
create type type_Opengauss_CAST_Case0034_1 as (t1 int, t2 text);
select cast('$2'::money as type_Opengauss_CAST_Case0034_1);
select cast(cast('$2'::money as unsigned) as type_Opengauss_CAST_Case0034_1);
-- 清理环境
drop type type_Opengauss_CAST_Case0034_1;
