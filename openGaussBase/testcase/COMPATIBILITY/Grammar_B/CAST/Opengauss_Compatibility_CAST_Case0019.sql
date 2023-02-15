-- @testpoint: cast用例,部分用例合理报错
-- as用逗号代替
--新建表
create table t_Opengauss_CAST_Case0019_1(a int,c money,b timestamp);
--插入数据
insert into t_Opengauss_CAST_Case0019_1 values(1,2,now());
insert into t_Opengauss_CAST_Case0019_1 values(2,'$33',now());
-- as用逗号代替
select cast(c , unsigned) from t_Opengauss_CAST_Case0019_1;
select cast(b , unsigned) from t_Opengauss_CAST_Case0019_1;
select cast(a , unsigned) from t_Opengauss_CAST_Case0019_1;
-- 清理环境
drop table t_Opengauss_CAST_Case0019_1;
