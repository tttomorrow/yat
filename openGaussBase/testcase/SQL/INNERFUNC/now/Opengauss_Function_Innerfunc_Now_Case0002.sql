-- @testpoint: now()给入参空值，合理报错
select now(null) from sys_dummy;
select now('') from sys_dummy;
