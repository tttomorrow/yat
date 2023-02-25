-- @testpoint:创建数据库,部分用例合理报错
create schema sch_Opengauss_DATABASE_Case0015_1;
-- 使用
use sch_Opengauss_DATABASE_Case0015_1;
select database();
-- use失败
use ;
select database();
-- 清理环境
drop schema sch_Opengauss_DATABASE_Case0015_1;
