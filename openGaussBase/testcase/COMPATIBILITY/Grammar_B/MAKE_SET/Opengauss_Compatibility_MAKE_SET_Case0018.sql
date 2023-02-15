-- @testpoint:关于make_set的事物场景测试,部分测试用例合理报错

-- 开启事物
start transaction;
-- make_set正常输入数值
select make_set(0,'a','b');
select make_set(31,'a','b','c','d','e','f');
select make_set(1,'a','b');
select make_set(1,null,'b');
select make_set(2,'a',null);
select make_set(31,'a','b','c','d');
select make_set(8,'a','b');
select make_set(3|1,'a','b','c','d');
select make_set(8&2,'a','b');
select make_set(12+1,'a','b');
select make_set(null,null,'b');
select make_set(null,'a',null);
select make_set(110,'a','b','c',null);
select make_set(0,'a','b','[2010-01-01 14:30, 2010-01-01 15:30)','e');
select make_set(null,'null','2022-09-03');
select make_set(0,'a','null','non est');
select make_set(3,1/8/1999,2022-09-03);
select make_set(3,null,true);
-- 提交
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(a,'a','b','c',null);
commit;
-- 1：开启事物2：执行make_set函数3：提交 
start transaction;
select make_set(,'a','b','c','d');
commit;
-- 1：开启事物2：执行make_set函数3：提交 
start transaction;
select make_set('','a','b','c','d');
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(0,'a','b','[2010-01-01 14:30, 2010-01-01 15:30)','e');
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(8&2,'a','b');
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(12+1,'2022-09-03','b');
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(null,'','2022-09-03');
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(0,'a','','non est');
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(null,'null','2022-09-03');
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(0,'a','null','non est');
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,3,2022-09-03);
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(null,1,4,6);
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,false,true);
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(null,trur);
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(0,2022-09-03);
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,1/8/1999,2022-09-03);
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,false,好);
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,￥￥,true);
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,false,);
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,);
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,false,null);
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,null,true);
commit;
-- 清理环境;expect: 清理环境成功
drop table if exists t_Opengauss_MAKE_SET_Case0018_1;
-- 创建表 expect:创建成功
create table t_Opengauss_MAKE_SET_Case0018_1(a int,b char(10));
-- 给表添加数据
insert into t_Opengauss_MAKE_SET_Case0018_1 values(1,'to'),(2,'xi'),(3,'dao'),(3,'to'),(4,'ruai'),(5,'mi'),(6,'fa'),(7,'xi'),(8,'xi'),(9,'la'),(10,'to'),(11,'no'),(11,'no'),(12,'buy'),(13,'buy'),(14,'buy'),(15,'bear'),(16,'bear');
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,false,1) from t_Opengauss_MAKE_SET_Case0018_1 where b='xix';
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(2,1+6,true) from t_Opengauss_MAKE_SET_Case0018_1 where b sounds like('t');
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(null,false,1,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0018_1 where b='xix';
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(1+1,false,1,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0018_1 where b='xix';
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(1+2,1+6,true,'hello') from t_Opengauss_MAKE_SET_Case0018_1 where b sounds like('t');
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(l,false,1,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0018_1 where b='xix';
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(r,1+6,true,'hello') from t_Opengauss_MAKE_SET_Case0018_1 where b sounds like('t');
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(00l,false,1,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0018_1 where b='xix';
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(011,1+6,true,'hello') from t_Opengauss_MAKE_SET_Case0018_1 where b sounds like('t');
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set('',false,1,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0018_1 where b='xix';
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set('',1+6,true,'hello') from t_Opengauss_MAKE_SET_Case0018_1 where b sounds like('t');
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set('',1|6,'a','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0018_1 where b='to';
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,'a','b') from t_Opengauss_MAKE_SET_Case0018_1 where b='xix';
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,'a','a') from t_Opengauss_MAKE_SET_Case0018_1 where b sounds like('t');
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,'b','b') from t_Opengauss_MAKE_SET_Case0018_1 where b='to';
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,'c','d') from t_Opengauss_MAKE_SET_Case0018_1 where b='xix';
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,'e','null') from t_Opengauss_MAKE_SET_Case0018_1 where b sounds like('t');
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,'too','null') from t_Opengauss_MAKE_SET_Case0018_1 where b='to';
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set('3','&',(select table_name from information_schema.tables where table_schema='public'));
commit;
-- 清理环境;expect: 清理环境成功
drop table t_Opengauss_MAKE_SET_Case0018_1;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,'&',(select table_name from information_schema.tables where table_schema='public'));
commit;
-- 创建表 expect:创建成功
create table t_Opengauss_MAKE_SET_Case0018_1(a int,b char(10));
create table t_Opengauss_MAKE_SET_Case0018_2(a int,b char(10));
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,'&',(select table_name from information_schema.tables where table_schema='public'));
commit;
-- 清理环境;expect: 清理环境成功
drop table t_Opengauss_MAKE_SET_Case0018_1;
drop table t_Opengauss_MAKE_SET_Case0018_2;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,'&',(select column_name from information_schema.columns where table_name='t_Opengauss_MAKE_SET_Case0018_1'));
commit;
-- 创建表 expect:创建成功
create table t_Opengauss_MAKE_SET_Case0018_1(a int);
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,'&',(select column_name from information_schema.columns where table_name='t_Opengauss_MAKE_SET_Case0018_1'));
commit;
-- 清理环境;expect: 清理环境成功
drop table t_Opengauss_MAKE_SET_Case0018_1;
-- 创建表 expect:创建成功
create table t_Opengauss_MAKE_SET_Case0018_1(a int,b char(10));
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,'&',(select column_name from information_schema.columns where table_name='t_Opengauss_MAKE_SET_Case0018_1'));
commit;
-- 清理环境;expect: 清理环境成功
drop table t_Opengauss_MAKE_SET_Case0018_1;
drop table if exists t_Opengauss_MAKE_SET_Case0018_1;
-- 创建表 expect:创建成功
create table t_Opengauss_MAKE_SET_Case0018_1(a int,b char(10));
-- 给表添加数据
insert into t_Opengauss_MAKE_SET_Case0018_1 values(1,null),(1,null),(1,null),(1,null),(2,'xi'),(3,'dao'),(3,'to'),(4,'ruai'),(5,'mi'),(6,'fa'),(7,'xi'),(8,'xi'),(9,'la'),(10,'to'),(11,'no'),(11,'no'),(12,'buy'),(13,'buy'),(14,'buy'),(15,'bear'),(16,'bear');
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,'&',(select b from public.t_Opengauss_MAKE_SET_Case0018_1));
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,'&',(select b from public.t_Opengauss_MAKE_SET_Case0018_1 where a=17));
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,'&',(select b from public.t_Opengauss_MAKE_SET_Case0018_1 where a=1));
commit;
-- 1：开启事物2：执行make_set函数3：提交
start transaction;
select make_set(3,'&',(select b from public.t_Opengauss_MAKE_SET_Case0018_1 where a=2));
commit;
-- 清理环境;expect: 清理环境成功
drop table t_Opengauss_MAKE_SET_Case0018_1;
















