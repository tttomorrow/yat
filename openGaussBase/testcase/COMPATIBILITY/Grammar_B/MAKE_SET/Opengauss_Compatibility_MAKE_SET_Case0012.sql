-- @testpoint:返回表的列bits位输入参数时make_set的运算,部分测试用例合理报错

-- 清理环境;expect: 清理环境成功
drop table if exists t_Opengauss_MAKE_SET_Case0012_1;
-- 创建表 expect:创建成功
create table t_Opengauss_MAKE_SET_Case0012_1(a int,b char(10));

-- 给表添加数据
insert into t_Opengauss_MAKE_SET_Case0012_1 values(1,'to'),(2,'xi'),(3,'dao'),(3,'to'),(4,'ruai'),(5,'mi'),(6,'fa'),(7,'xi'),(8,'xi'),(9,'la'),(10,'to'),(11,'no'),(11,'no'),(12,'buy'),(13,'buy'),(14,'buy'),(15,'bear'),(16,'bear');

-- 输入合理范围内的数字
select make_set(0,false,1) from t_Opengauss_MAKE_SET_Case0012_1 where b='xix';
select make_set(0,false,1) from t_Opengauss_MAKE_SET_Case0012_1 where b sounds like('t');
select make_set(0,false,1) from t_Opengauss_MAKE_SET_Case0012_1 where b='to';
select make_set(0,false,1) from t_Opengauss_MAKE_SET_Case0012_1 where b='xi';

select make_set(3,false,1) from t_Opengauss_MAKE_SET_Case0012_1 where b='xix';
select make_set(2,1+6,true) from t_Opengauss_MAKE_SET_Case0012_1 where b sounds like('t');
select make_set(1,1|6,'a') from t_Opengauss_MAKE_SET_Case0012_1 where b='to';
select make_set(7,'hello','world') from t_Opengauss_MAKE_SET_Case0012_1 where b='xi';

select make_set(2147483649,false,1,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0012_1 where b='xix';
select make_set(2147483651,1+6,true,'hello') from t_Opengauss_MAKE_SET_Case0012_1 where b sounds like('t');
select make_set(2147483659,1|6,'a','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0012_1 where b='to';
select make_set(-2147483659,'hello','world') from t_Opengauss_MAKE_SET_Case0012_1 where b='xi';
select make_set(-2147483649,1|6,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0012_1 where b='to';

-- 输入null
select make_set(null,false,1,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0012_1 where b='xix';
select make_set(null,1+6,true,'hello') from t_Opengauss_MAKE_SET_Case0012_1 where b sounds like('t');
select make_set(null,1|6,'a','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0012_1 where b='to';
select make_set(null,'hello','world') from t_Opengauss_MAKE_SET_Case0012_1 where b='xi';
select make_set(null,1|6,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0012_1 where b='to';

-- 输入数字运算
select make_set(1+1,false,1,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0012_1 where b='xix';
select make_set(1+2,1+6,true,'hello') from t_Opengauss_MAKE_SET_Case0012_1 where b sounds like('t');
select make_set(7&9,1|6,'a','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0012_1 where b='to';
select make_set(9/3,'hello','world') from t_Opengauss_MAKE_SET_Case0012_1 where b='xi';
select make_set(9/4,1|6,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0012_1 where b='to';
select make_set(9/5,1|6,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0012_1 where b='to';
select make_set(9/6,1|6,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0012_1 where b='to';

-- 输入字母或其他
select make_set(l,false,1,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0012_1 where b='xix';
select make_set(r,1+6,true,'hello') from t_Opengauss_MAKE_SET_Case0012_1 where b sounds like('t');
select make_set(-,1|6,'a','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0012_1 where b='to';
select make_set(!,'hello','world') from t_Opengauss_MAKE_SET_Case0012_1 where b='xi';
select make_set(&,1|6,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0012_1 where b='to';

-- 输入二进制
select make_set(00l,false,1,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0012_1 where b='xix';
select make_set(011,1+6,true,'hello') from t_Opengauss_MAKE_SET_Case0012_1 where b sounds like('t');
select make_set(111,1|6,'a','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0012_1 where b='to';
select make_set(100,'hello','world') from t_Opengauss_MAKE_SET_Case0012_1 where b='xi';
select make_set(101,1|6,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0012_1 where b='to';

-- 清理环境
drop table t_Opengauss_MAKE_SET_Case0012_1;
