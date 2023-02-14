-- @testpoint:返回表的列str位不加单引号时make_set的运算,部分测试用例合理报错

-- 清理环境;expect: 清理环境成功
drop table if exists t_Opengauss_MAKE_SET_Case0014_1;
-- 创建表 expect:创建成功
create table t_Opengauss_MAKE_SET_Case0014_1(a int,b char(10));

-- 给表添加数据
insert into t_Opengauss_MAKE_SET_Case0014_1 values(1,null),(1,null),(1,null),(1,null),(2,'xi'),(3,'dao'),(3,'to'),(4,'ruai'),(5,'mi'),(6,'fa'),(7,'xi'),(8,'xi'),(9,'la'),(10,'to'),(11,'no'),(11,'no'),(12,'buy'),(13,'buy'),(14,'buy'),(15,'bear'),(16,'bear');

-- 输入表中不存在的字段
select make_set(3,a1,b1) from t_Opengauss_MAKE_SET_Case0014_1 where b='xix';
select make_set(3,sr,c) from t_Opengauss_MAKE_SET_Case0014_1 where b sounds like('t');
select make_set(3,fa,dao) from t_Opengauss_MAKE_SET_Case0014_1 where b='to';
select make_set(3,ruai,mi) from t_Opengauss_MAKE_SET_Case0014_1 where b='xi';

-- 不输入
select make_set(3,) from t_Opengauss_MAKE_SET_Case0014_1 where b='xix';
select make_set(3,) from t_Opengauss_MAKE_SET_Case0014_1 where b sounds like('t');
select make_set(3,) from t_Opengauss_MAKE_SET_Case0014_1 where b='to';
select make_set(3,) from t_Opengauss_MAKE_SET_Case0014_1 where b='xi';

-- 输入表中存在的字段
select make_set(3,a,b) from t_Opengauss_MAKE_SET_Case0014_1 where b='xix';
select make_set(3,a,a) from t_Opengauss_MAKE_SET_Case0014_1 where b sounds like('t');
select make_set(3,b,b) from t_Opengauss_MAKE_SET_Case0014_1 where b='to';
select make_set(3,a,b) from t_Opengauss_MAKE_SET_Case0014_1 where a=1;
select make_set(3,b,b) from t_Opengauss_MAKE_SET_Case0014_1 where a=1;
select make_set(3,a,b) from t_Opengauss_MAKE_SET_Case0014_1 where a=5;
select make_set(3,b,b) from t_Opengauss_MAKE_SET_Case0014_1 where b='buy';

-- 清理环境;expect: 清理环境成功
drop table t_Opengauss_MAKE_SET_Case0014_1;



