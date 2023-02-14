-- @testpoint:database函数输入参数,部分用例合理报错
-- 创建模式
create schema sch_Opengauss_DATABASE_Case0004_1;
create schema sch_Opengauss_DATABASE_Case0004_2;
create schema sch_Opengauss_DATABASE_Case0004_3;
-- 选择当前数据库并且显示当前数据库
select database(1);
use sch_Opengauss_DATABASE_Case0004_1;
select database(null);
use sch_Opengauss_DATABASE_Case0004_2;
select database('sch_Opengauss_DATABASE_Case0004_2');
use sch_Opengauss_DATABASE_Case0004_3;
select database(sch_Opengauss_DATABASE_Case0004_3);
-- 清理环境
drop schema sch_Opengauss_DATABASE_Case0004_1;
drop schema sch_Opengauss_DATABASE_Case0004_2;
drop schema sch_Opengauss_DATABASE_Case0004_3;
