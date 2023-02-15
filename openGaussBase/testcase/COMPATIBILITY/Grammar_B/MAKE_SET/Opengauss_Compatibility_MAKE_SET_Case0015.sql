-- @testpoint:返回表的列str位加单引号时make_set的运算,部分测试用例合理报错

-- 清理环境;expect: 清理环境成功
drop table if exists t_Opengauss_MAKE_SET_Case0015_1;
-- 创建表 expect:创建成功
create table t_Opengauss_MAKE_SET_Case0015_1(a int,b char(10));
-- 给表添加数据
insert into t_Opengauss_MAKE_SET_Case0015_1 values(1,'to'),(2,'xi'),(3,'dao'),(3,'to'),(4,'ruai'),(5,'mi'),(6,'fa'),(7,'xi'),(8,'xi'),(9,'la'),(10,'to'),(11,'no'),(11,'no'),(12,'buy'),(13,'buy'),(14,'buy'),(15,'bear'),(16,'bear');
-- 输入表中字段
select make_set(3,'a','b') from t_Opengauss_MAKE_SET_Case0015_1 where b='xix';
select make_set(3,'a','a') from t_Opengauss_MAKE_SET_Case0015_1 where b sounds like('t');
select make_set(3,'b','b') from t_Opengauss_MAKE_SET_Case0015_1 where b='to';
select make_set(3,'a') from t_Opengauss_MAKE_SET_Case0015_1 where b='xi';
select make_set(7,'a','b','b','a','a') from t_Opengauss_MAKE_SET_Case0015_1 where b='to';
-- 不输入
select make_set(3,'','') from t_Opengauss_MAKE_SET_Case0015_1 where b='xix';
select make_set(3,'','') from t_Opengauss_MAKE_SET_Case0015_1 where b sounds like('t');
select make_set(3,'','b') from t_Opengauss_MAKE_SET_Case0015_1 where b='to';
select make_set(3,'') from t_Opengauss_MAKE_SET_Case0015_1 where b='xi';
select make_set(7,'','','','','') from t_Opengauss_MAKE_SET_Case0015_1 where b='to';
-- 输入表中不存在的字段
select make_set(3,'c','d') from t_Opengauss_MAKE_SET_Case0015_1 where b='xix';
select make_set(3,'e','null') from t_Opengauss_MAKE_SET_Case0015_1 where b sounds like('t');
select make_set(3,'too','null') from t_Opengauss_MAKE_SET_Case0015_1 where b='to';
select make_set(3,'fine') from t_Opengauss_MAKE_SET_Case0015_1 where b='xi';
select make_set(25,'go','int','str','time','do') from t_Opengauss_MAKE_SET_Case0015_1 where b='to';
-- 清理环境;expect: 清理环境成功
drop table t_Opengauss_MAKE_SET_Case0015_1;

