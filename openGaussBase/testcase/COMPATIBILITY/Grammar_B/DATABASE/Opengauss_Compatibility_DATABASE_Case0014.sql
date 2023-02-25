-- @testpoint:选择不存在的数据库,部分用例合理报错
use sch_Opengauss_DATABASE_Case0014_1;
select database();
-- use失败选择数据库
use ;
select database();

