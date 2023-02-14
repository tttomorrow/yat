-- @testpoint:在视图中make_set的运算,部分用例合理报错
-- 清理环境;expect: 清理环境成功
drop table if exists t_Opengauss_MAKE_SET_Case0019_1;
-- 创建表 expect:创建成功
create table t_Opengauss_MAKE_SET_Case0019_1(a int,b char(10));
-- 给表添加数据
insert into t_Opengauss_MAKE_SET_Case0019_1 values(1,'to'),(2,'xi'),(3,'dao'),(3,'to'),(4,'ruai'),(5,'mi'),(6,'fa'),(7,'xi'),(8,'xi'),(9,'la'),(10,'to'),(11,'no'),(11,'no'),(12,'buy'),(13,'buy'),(14,'buy'),(15,'bear'),(16,'bear');
-- 创建视图
create view v_Opengauss_MAKE_SET_Case0019_1 as select * from t_Opengauss_MAKE_SET_Case0019_1;
-- 在视图中执行make_set函数
select make_set(3,false,1) from v_Opengauss_MAKE_SET_Case0019_1 where b='xix';
select make_set(2,1+6,true) from v_Opengauss_MAKE_SET_Case0019_1 where b sounds like('t');
select make_set(null,false,1,'hello','hello','hello','hello') from v_Opengauss_MAKE_SET_Case0019_1 where b='xix';
select make_set(1+1,false,1,'hello','hello','hello','hello') from v_Opengauss_MAKE_SET_Case0019_1 where b='xix';
select make_set(1+2,1+6,true,'hello') from v_Opengauss_MAKE_SET_Case0019_1 where b sounds like('t');
select make_set(l,false,1,'hello','hello','hello','hello') from v_Opengauss_MAKE_SET_Case0019_1 where b='xix';
select make_set(r,1+6,true,'hello') from v_Opengauss_MAKE_SET_Case0019_1 where b sounds like('t');
select make_set(00l,false,1,'hello','hello','hello','hello') from v_Opengauss_MAKE_SET_Case0019_1 where b='xix';
select make_set(011,1+6,true,'hello') from v_Opengauss_MAKE_SET_Case0019_1 where b sounds like('t');
select make_set('',false,1,'hello','hello','hello','hello') from v_Opengauss_MAKE_SET_Case0019_1 where b='xix';
select make_set('',1+6,true,'hello') from v_Opengauss_MAKE_SET_Case0019_1 where b sounds like('t');
select make_set('',1|6,'a','hello','hello','hello') from v_Opengauss_MAKE_SET_Case0019_1 where b='to';
select make_set(,false,1,'hello','hello','hello','hello') from v_Opengauss_MAKE_SET_Case0019_1 where b='xix';
select make_set(,1+6,true,'hello') from v_Opengauss_MAKE_SET_Case0019_1 where b sounds like('t');
select make_set(,1|6,'a','hello','hello','hello') from v_Opengauss_MAKE_SET_Case0019_1 where b='to';
select make_set(,'hello','world') from v_Opengauss_MAKE_SET_Case0019_1 where b='xi';
select make_set(3,a1,b1) from v_Opengauss_MAKE_SET_Case0019_1 where b='xix';
select make_set(3,sr,c) from v_Opengauss_MAKE_SET_Case0019_1 where b sounds like('t');
select make_set(3,fa,dao) from v_Opengauss_MAKE_SET_Case0019_1 where b='to';
select make_set(3,) from v_Opengauss_MAKE_SET_Case0019_1 where b='xix';
select make_set(3,) from v_Opengauss_MAKE_SET_Case0019_1 where b sounds like('t');
select make_set(3,) from v_Opengauss_MAKE_SET_Case0019_1 where b='to';
select make_set(3,a,b) from v_Opengauss_MAKE_SET_Case0019_1 where b='xix';
select make_set(3,a,a) from v_Opengauss_MAKE_SET_Case0019_1 where b sounds like('t');
select make_set(3,b,b) from v_Opengauss_MAKE_SET_Case0019_1 where b='to';
select make_set(3,a,b) from v_Opengauss_MAKE_SET_Case0019_1 where a=1;
select make_set(3,'a','b') from v_Opengauss_MAKE_SET_Case0019_1 where b='xix';
select make_set(3,'a','a') from v_Opengauss_MAKE_SET_Case0019_1 where b sounds like('t');
select make_set(3,'b','b') from v_Opengauss_MAKE_SET_Case0019_1 where b='to';
select make_set(3,'','') from v_Opengauss_MAKE_SET_Case0019_1 where b='xix';
select make_set(3,'','') from v_Opengauss_MAKE_SET_Case0019_1 where b sounds like('t');
select make_set(3,'','b') from v_Opengauss_MAKE_SET_Case0019_1 where b='to';
select make_set(3,'c','d') from v_Opengauss_MAKE_SET_Case0019_1 where b='xix';
select make_set(3,'e','null') from v_Opengauss_MAKE_SET_Case0019_1 where b sounds like('t');
select make_set(3,'too','null') from v_Opengauss_MAKE_SET_Case0019_1 where b='to';
select make_set(3,'&',(select column_name from information_schema.columns where table_name='v_Opengauss_MAKE_SET_Case0019_1'));
-- 清理环境;expect: 清理环境成功
drop view v_Opengauss_MAKE_SET_Case0019_1;
drop table t_Opengauss_MAKE_SET_Case0019_1;
-- 创建表 expect:创建成功
create table t_Opengauss_MAKE_SET_Case0019_1(a int);
-- 创建视图
create view v_Opengauss_MAKE_SET_Case0019_1 as select * from t_Opengauss_MAKE_SET_Case0019_1;
-- 在视图中执行make_set函数
select make_set(3,'&',(select column_name from information_schema.columns where table_name='v_Opengauss_MAKE_SET_Case0019_1'));
-- 清理环境;expect: 清理环境成功
drop view v_Opengauss_MAKE_SET_Case0019_1;
drop table t_Opengauss_MAKE_SET_Case0019_1;
-- 在不存在的表中执行make_set函数
select make_set(3,'&',(select (column_name) from information_schema.columns where table_name='t_Opengauss_MAKE_SET_Case0019_1'));



