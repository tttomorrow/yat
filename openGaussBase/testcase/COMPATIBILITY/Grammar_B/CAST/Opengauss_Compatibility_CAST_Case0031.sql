-- @testpoint: cast用例,部分用例合理报错
-- 隐式转换
-- 新建表
create table t_Opengauss_CAST_Case0031_1(a int,b money,c timestamp);
-- 插入数据
insert into t_Opengauss_CAST_Case0031_1 values(1,33::money,'2020-09-28'::timestamp);
insert into t_Opengauss_CAST_Case0031_1 values(1,'$3'::unsigned,'2020-09-28'::timestamp);
insert into t_Opengauss_CAST_Case0031_1 values(1,3::unsigned,'2020-09-28'::timestamp);
insert into t_Opengauss_CAST_Case0031_1 values(1,'2020-09-28'::money,'2020-09-28'::timestamp);
insert into t_Opengauss_CAST_Case0031_1 values(1,'15.15'::unsigned::money,'2020-09-28'::unsigned::timestamp);
insert into t_Opengauss_CAST_Case0031_1 values(1,'15.15'::unsigned::money,cast('2020-09-28' as unsigned)::timestamp);
--清理环境
drop table t_Opengauss_CAST_Case0031_1;
