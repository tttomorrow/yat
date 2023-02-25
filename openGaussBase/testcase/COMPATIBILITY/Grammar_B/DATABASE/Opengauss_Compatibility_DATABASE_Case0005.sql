-- @testpoint:删除当前模式，显示数据库
-- 创建模式
create schema sch_Opengauss_DATABASE_Case0005_1;
create schema sch_Opengauss_DATABASE_Case0005_2;
-- 选择使用存在的数据库
use sch_Opengauss_DATABASE_Case0005_1;
-- 删除当前使用数据库
drop schema sch_Opengauss_DATABASE_Case0005_1;
-- 显示当前使用的数据库
select database();
-- 选择使用存在的数据库
use sch_Opengauss_DATABASE_Case0005_2;
-- 删除当前使用数据库
drop schema sch_Opengauss_DATABASE_Case0005_2;
-- 显示当前使用的数据库
select database();
