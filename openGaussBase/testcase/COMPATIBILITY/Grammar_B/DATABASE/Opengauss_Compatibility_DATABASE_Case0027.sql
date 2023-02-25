-- @testpoint:删除当前模式，重新选择数据库并且显示数据库
-- 创建模式
create schema sch_Opengauss_DATABASE_Case0027_1;
create schema sch_Opengauss_DATABASE_Case0027_2;
-- 选择使用存在的数据库
use sch_Opengauss_DATABASE_Case0027_1;
-- 删除当前使用数据库
drop schema sch_Opengauss_DATABASE_Case0027_1;
-- 显示当前使用的数据库
select database();
-- 选择使用存在的数据库
use sch_Opengauss_DATABASE_Case0027_2;
-- 显示当前使用的数据库
select database();
-- 清理环境
drop schema sch_Opengauss_DATABASE_Case0027_2;
