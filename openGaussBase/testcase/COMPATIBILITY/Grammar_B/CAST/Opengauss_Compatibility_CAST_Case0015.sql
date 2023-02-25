-- @testpoint: cast用例,部分用例合理报错
--转换存在表的多个字段
--新建表
create table t_Opengauss_CAST_Case0015_1(a int,c money,b timestamp);
--插入数据
insert into t_Opengauss_CAST_Case0015_1 values(1,2,now());
insert into t_Opengauss_CAST_Case0015_1 values(2,'$33',now());
--转换存在表的多个字段
select cast(a,c as unsigned) from t_Opengauss_CAST_Case0015_1;
select cast(a c as unsigned) from t_Opengauss_CAST_Case0015_1;
select cast(c,b as unsigned) from t_Opengauss_CAST_Case0015_1;
select cast(c b as unsigned) from t_Opengauss_CAST_Case0015_1;
--清理环境
drop table t_Opengauss_CAST_Case0015_1;
