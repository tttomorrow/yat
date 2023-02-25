-- @testpoint:创建模式
create schema sch_Opengauss_DATABASE_Case0009_1;
create schema sch_Opengauss_DATABASE_Case0009_2;
create schema sch_Opengauss_DATABASE_Case0009_3;
--选择存在的数据库
use sch_Opengauss_DATABASE_Case0009_1;
-- 查询当前数据库
select database();
--选择存在的数据库
use sch_Opengauss_DATABASE_Case0009_2;
-- 查询当前数据库
select database();
--选择存在的数据库
use sch_Opengauss_DATABASE_Case0009_3;
-- 查询当前数据库
select database();
-- 清理环境
drop schema sch_Opengauss_DATABASE_Case0009_1;
drop schema sch_Opengauss_DATABASE_Case0009_2;
drop schema sch_Opengauss_DATABASE_Case0009_3;
