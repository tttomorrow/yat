-- @testpoint: cast用例,部分用例合理报错
-- 转换不存在表中的某个字段
--新建表
create table t_Opengauss_CAST_Case0013_1(a int,c money,b timestamp);
--插入数据
insert into t_Opengauss_CAST_Case0013_1 values(1,2,now());
insert into t_Opengauss_CAST_Case0013_1 values(2,'$33',now());
-- 转换不存在表中的某个字段
select cast(d as unsigned) from t_Opengauss_CAST_Case0013_2;
select cast(e as unsigned) from t_Opengauss_CAST_Case0013_3;
select cast(f as unsigned) from t_Opengauss_CAST_Case0013_4;
-- 清理环境
drop table t_Opengauss_CAST_Case0013_1;
