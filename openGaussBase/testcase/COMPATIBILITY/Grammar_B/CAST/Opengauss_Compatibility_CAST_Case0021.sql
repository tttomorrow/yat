-- @testpoint: cast用例,部分用例合理报错
-- as前后均为expr
--新建表
create table t_Opengauss_CAST_Case0021_1(a int,c money,b timestamp);
--插入数据
insert into t_Opengauss_CAST_Case0021_1 values(1,2,now());
insert into t_Opengauss_CAST_Case0021_1 values(2,'$33',now());
-- as前后均为expr
select cast(1 as 0) from t_Opengauss_CAST_Case0021_1;
select cast(false as 0) from t_Opengauss_CAST_Case0021_1;
select cast(true as 0) from t_Opengauss_CAST_Case0021_1;
select cast(b as true) from t_Opengauss_CAST_Case0021_1;
select cast(true as b) from t_Opengauss_CAST_Case0021_1;
-- 清理环境
drop table t_Opengauss_CAST_Case0021_1;
