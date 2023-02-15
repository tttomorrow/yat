-- @testpoint:创建模式
create schema sch_Opengauss_DATABASE_Case0021_1;
create schema sch_Opengauss_DATABASE_Case0021_2;
create schema sch_Opengauss_DATABASE_Case0021_3;
--选择不存在的数据库
use sch_Opengauss_DATABASE_Case0021_4;
-- 查询当前数据库
select database();
--选择不存在的数据库
use sch_Opengauss_DATABASE_Case0021_5;
-- 查询当前数据库
select database();
-- 清理环境
drop schema sch_Opengauss_DATABASE_Case0021_1;
drop schema sch_Opengauss_DATABASE_Case0021_2;
drop schema sch_Opengauss_DATABASE_Case0021_3;
