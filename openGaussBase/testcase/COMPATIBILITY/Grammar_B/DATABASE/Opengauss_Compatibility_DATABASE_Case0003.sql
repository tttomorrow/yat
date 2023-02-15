-- @testpoint:创建数据库
create schema sch_Opengauss_DATABASE_Case0003_1;
create schema sch_Opengauss_DATABASE_Case0003_2;
create schema sch_Opengauss_DATABASE_Case0003_3;
create schema sch_Opengauss_DATABASE_Case0003_4;
create schema sch_Opengauss_DATABASE_Case0003_5;
-- 选择使用的的数据库并显示当前当前数据库
use sch_Opengauss_DATABASE_Case0003_1;
select database();
use sch_Opengauss_DATABASE_Case0003_2;
select database();
use sch_Opengauss_DATABASE_Case0003_3;
select database();
use sch_Opengauss_DATABASE_Case0003_4;
select database();
use sch_Opengauss_DATABASE_Case0003_5;
select database();
use public;
select database();
-- 清理环境
drop schema sch_Opengauss_DATABASE_Case0003_1;
drop schema sch_Opengauss_DATABASE_Case0003_2;
drop schema sch_Opengauss_DATABASE_Case0003_3;
drop schema sch_Opengauss_DATABASE_Case0003_4;
drop schema sch_Opengauss_DATABASE_Case0003_5;
