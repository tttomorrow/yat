-- @testpoint: now()给多个入参，合理报错
select now(1,2) from sys_dummy;
select now(1,2,3,45,6) from sys_dummy;