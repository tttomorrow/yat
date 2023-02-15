-- @testpoint: cast用例
set time zone 'uct';
-- 转换数据后查看原始数据
--新建表
create table t_Opengauss_CAST_Case0017_1(a int,c money,b timestamp);
--插入数据
insert into t_Opengauss_CAST_Case0017_1 values(1,2,'12-11-09');
insert into t_Opengauss_CAST_Case0017_1 values(2,'$33','12-11-09');
--查询当前数据
select * from t_Opengauss_CAST_Case0017_1;
-- 转换存在表的某个存在字段
select cast(c as unsigned) from t_Opengauss_CAST_Case0017_1;
set time zone 'uct';
select cast(b as unsigned) from t_Opengauss_CAST_Case0017_1;
select cast(a as unsigned) from t_Opengauss_CAST_Case0017_1;
-- 转换数据后查看原始数据
select * from t_Opengauss_CAST_Case0017_1;
-- 清理环境
drop table t_Opengauss_CAST_Case0017_1;
