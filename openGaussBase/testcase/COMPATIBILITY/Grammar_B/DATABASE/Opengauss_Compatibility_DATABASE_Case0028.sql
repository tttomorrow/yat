-- @testpoint:选择不存在的数据库，部分用例合理报错
use schmea_Opengauss_DATABASE_Case0028_1;
select database();
use schmea_Opengauss_DATABASE_Case0028_2;
select database();
