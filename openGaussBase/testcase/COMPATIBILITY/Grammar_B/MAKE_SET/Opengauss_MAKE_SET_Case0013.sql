-- @testpoint:返回表的列bits位不输入参数时make_set的运算,部分测试用例合理报错

-- 清理环境;expect: 清理环境成功
drop table if exists t_Opengauss_MAKE_SET_Case0013_1;
-- 创建表 expect:创建成功
create table t_Opengauss_MAKE_SET_Case0013_1(a int,b char(10));

-- 给表添加数据
insert into t_Opengauss_MAKE_SET_Case0013_1 values(1,'to'),(2,'xi'),(3,'dao'),(3,'to'),(4,'ruai'),(5,'mi'),(6,'fa'),(7,'xi'),(8,'xi'),(9,'la'),(10,'to'),(11,'no'),(11,'no'),(12,'buy'),(13,'buy'),(14,'buy'),(15,'bear'),(16,'bear');

-- 有单引号
select make_set('',false,1,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0013_1 where b='xix';
select make_set('',1+6,true,'hello') from t_Opengauss_MAKE_SET_Case0013_1 where b sounds like('t');
select make_set('',1|6,'a','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0013_1 where b='to';
select make_set('','hello','world') from t_Opengauss_MAKE_SET_Case0013_1 where b='xi';
select make_set('',1|6,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0013_1 where b='to';

-- 无单引号
select make_set(,false,1,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0013_1 where b='xix';
select make_set(,1+6,true,'hello') from t_Opengauss_MAKE_SET_Case0013_1 where b sounds like('t');
select make_set(,1|6,'a','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0013_1 where b='to';
select make_set(,'hello','world') from t_Opengauss_MAKE_SET_Case0013_1 where b='xi';
select make_set(,1|6,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0013_1 where b='to';

-- 清理环境;expect: 清理环境成功
drop table t_Opengauss_MAKE_SET_Case0013_1;
