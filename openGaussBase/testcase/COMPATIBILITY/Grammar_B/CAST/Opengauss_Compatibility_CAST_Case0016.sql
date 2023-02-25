-- @testpoint: cast用例,部分用例合理报错
set time zone 'uct';
-- 转换存在表的某个存在字段
--新建表
create table t_Opengauss_CAST_Case0016_1(a int,c money,b timestamp);
--插入数据
insert into t_Opengauss_CAST_Case0016_1 values(1,2,'12-11-09');
insert into t_Opengauss_CAST_Case0016_1 values(2,'$33','12-11-09');
-- 转换存在表的某个存在字段
select cast(c as unsigned) from t_Opengauss_CAST_Case0016_1;
select cast(b as unsigned) from t_Opengauss_CAST_Case0016_1;
select cast(a as unsigned) from t_Opengauss_CAST_Case0016_1;
-- 清理环境
drop table t_Opengauss_CAST_Case0016_1;
