-- @testpoint:选择数据库并且使用参数,部分用例合理报错
select database(public);
use sch_Opengauss_DATABASE_Case0017_1;
select database(null);
use sch_Opengauss_DATABASE_Case0017_2;
select database('sch_Opengauss_DATABASE_Case0017_2');
use sch_Opengauss_DATABASE_Case0017_3;
select database(sch_Opengauss_DATABASE_Case0017_3);
