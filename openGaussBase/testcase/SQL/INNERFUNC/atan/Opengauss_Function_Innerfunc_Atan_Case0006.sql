-- @testpoint: 无输入，无效参数，合理报错


select atan('') from sys_dummy;
select atan(null) from sys_dummy;

select atan() from sys_dummy;
select atan('11+11') from sys_dummy;
select atan(11 11) from sys_dummy;
select atan(11,11) from sys_dummy;
select atan(,) from sys_dummy;
