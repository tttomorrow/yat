-- @testpoint:创建数据库
create schema sch_Opengauss_DATABASE_Case0016_1;
create schema sch_Opengauss_DATABASE_Case0016_2;
create schema sch_Opengauss_DATABASE_Case0016_3;
-- 选择使用的的数据库并显示当前当前数据库
use sch_Opengauss_DATABASE_Case0016_1;
select database();
use sch_Opengauss_DATABASE_Case0016_2;
select database();
use sch_Opengauss_DATABASE_Case0016_3;
select database();
-- 清理环境
drop schema sch_Opengauss_DATABASE_Case0016_1;
drop schema sch_Opengauss_DATABASE_Case0016_2;
drop schema sch_Opengauss_DATABASE_Case0016_3;
