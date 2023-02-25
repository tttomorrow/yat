-- @testpoint:make_set的查询场景测试,部分测试用例合理报错
-- 清理环境;expect: 清理环境成功
drop table if exists t_Opengauss_MAKE_SET_Case0017_1;
-- 创建表 expect:创建成功
create table t_Opengauss_MAKE_SET_Case0017_1(a int,b char(10));
-- 给表添加数据
insert into t_Opengauss_MAKE_SET_Case0017_1 values(1,null),(1,null),(1,null),(1,null),(2,'xi'),(3,'dao'),(3,'to'),(4,'ruai'),(5,'mi'),(6,'fa'),(7,'xi'),(8,'xi'),(9,'la'),(10,'to'),(11,'no'),(11,'no'),(12,'buy'),(13,'buy'),(14,'buy'),(15,'bear'),(16,'bear');
-- 不支持查询当前使用的数据库
select make_set(3,'&',(select database()));
-- 清理环境;expect: 清理环境成功
drop table if exists t_Opengauss_MAKE_SET_Case0017_1;
-- 没有表时查询字段名
select make_set(3,'&',(select column_name from information_schema.columns where table_name='t_Opengauss_MAKE_SET_Case0017_1'));
-- 创建表 expect:创建成功
create table t_Opengauss_MAKE_SET_Case0017_1(a int);
-- 有一个字段的表查询字段名
select make_set(3,'&',(select column_name from information_schema.columns where table_name='t_Opengauss_MAKE_SET_Case0017_1'));
-- 清理环境;expect: 清理环境成功
drop table t_Opengauss_MAKE_SET_Case0017_1;
-- 创建表 expect:创建成功
create table t_Opengauss_MAKE_SET_Case0017_1(a int,b char(10));
-- 有多个字段的表查询字段名
select make_set(3,'&',(select column_name from information_schema.columns where table_name='t_Opengauss_MAKE_SET_Case0017_1'));
-- 清理环境;expect: 清理环境成功
drop table t_Opengauss_MAKE_SET_Case0017_1;
-- 查询字段数据
-- 清理环境;expect: 清理环境成功
drop table if exists t_Opengauss_MAKE_SET_Case0017_1;
-- 创建表 expect:创建成功
create table t_Opengauss_MAKE_SET_Case0017_1(a int,b char(10));
-- 给表添加数据
insert into t_Opengauss_MAKE_SET_Case0017_1 values(1,null),(1,null),(1,null),(1,null),(2,'xi'),(3,'dao'),(3,'to'),(4,'ruai'),(5,'mi'),(6,'fa'),(7,'xi'),(8,'xi'),(9,'la'),(10,'to'),(11,'no'),(11,'no'),(12,'buy'),(13,'buy'),(14,'buy'),(15,'bear'),(16,'bear');
-- 查询字段数据
select make_set(3,'&',(select b from t_Opengauss_MAKE_SET_Case0017_1));
select make_set(3,'&',(select b from t_Opengauss_MAKE_SET_Case0017_1 where a=17));
select make_set(3,'&',(select b from t_Opengauss_MAKE_SET_Case0017_1 where a=1));
select make_set(3,'&',(select b from t_Opengauss_MAKE_SET_Case0017_1 where a=2));
-- 清理环境;expect: 清理环境成功
drop table t_Opengauss_MAKE_SET_Case0017_1;


