-- @testpoint: cast用例,部分用例合理报错
-- as前为expr，后为自定义type
--定义数据类型
create type type_Opengauss_CAST_Case0025_1 as (t_Opengauss_CAST_Case0025_1 int, t2 text);
--新建表
create table t_Opengauss_CAST_Case0025_1(a int,c money,b timestamp);
--插入数据
insert into t_Opengauss_CAST_Case0025_1 values(1,2,now());
insert into t_Opengauss_CAST_Case0025_1 values(2,'$33',now());
-- 转换存在表的某个存在字段
select cast(c as type_Opengauss_CAST_Case0025_1) from t_Opengauss_CAST_Case0025_1;
select cast(b as type_Opengauss_CAST_Case0025_1) from t_Opengauss_CAST_Case0025_1;
select cast(a as type_Opengauss_CAST_Case0025_1) from t_Opengauss_CAST_Case0025_1;
-- 清理环境
drop table t_Opengauss_CAST_Case0025_1;
