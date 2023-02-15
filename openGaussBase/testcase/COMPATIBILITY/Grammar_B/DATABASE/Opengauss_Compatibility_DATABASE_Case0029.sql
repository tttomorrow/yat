-- @testpoint:创建数据库
create schema sch_Opengauss_DATABASE_Case0029_1;
create schema sch_Opengauss_DATABASE_Case0029_2;
create schema sch_Opengauss_DATABASE_Case0029_3;
create schema sch_Opengauss_DATABASE_Case0029_4;
create schema sch_Opengauss_DATABASE_Case0029_5;
-- 选择使用的的数据库并显示当前当前数据库
use sch_Opengauss_DATABASE_Case0029_1;
select database();
use sch_Opengauss_DATABASE_Case0029_2;
select database();
use sch_Opengauss_DATABASE_Case0029_3;
select database();
use sch_Opengauss_DATABASE_Case0029_4;
select database();
use sch_Opengauss_DATABASE_Case0029_5;
select database();
use public;
select database();
-- 清理环境
drop schema sch_Opengauss_DATABASE_Case0029_1;
drop schema sch_Opengauss_DATABASE_Case0029_2;
drop schema sch_Opengauss_DATABASE_Case0029_3;
drop schema sch_Opengauss_DATABASE_Case0029_4;
drop schema sch_Opengauss_DATABASE_Case0029_5;
