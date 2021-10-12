-- @testpoint: max函数参数异常校验，合理报错
select max() from sys_dummy;
select max(1,2) from sys_dummy;
select max(1,'&^%') from sys_dummy;
select max('pst'::timestamp with time zone) from sys_dummy;
