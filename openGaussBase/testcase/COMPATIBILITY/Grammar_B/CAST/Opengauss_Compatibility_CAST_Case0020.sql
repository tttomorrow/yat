-- @testpoint: cast用例
-- as前为type，as后为expr(0/1,true/false)
-- 新建表
create table t_Opengauss_CAST_Case0020_1(a int,c money,b timestamp);
-- 插入数据
insert into t_Opengauss_CAST_Case0020_1 values(1,2,now());
insert into t_Opengauss_CAST_Case0020_1 values(2,'$33',now());
-- as前为type，as后为expr(0/1,true/false)
select cast(0 as unsigned) from t_Opengauss_CAST_Case0020_1;
select cast(true as unsigned) from t_Opengauss_CAST_Case0020_1;
select cast(1 as unsigned) from t_Opengauss_CAST_Case0020_1;
-- 清理环境
drop table t_Opengauss_CAST_Case0020_1;
