-- @testpoint: 输入为有效边界值


select atan2(cast(-9223372036854775808 as bigint),tan(cast(9223372036854775807 as bigint))) from sys_dummy;
select atan2(cast(-2147483648 as integer),tan(cast(2147483647 as integer))) from sys_dummy;
select atan2(cast(1.0E-127 as decimal),tan(cast(1.0E-128 as decimal))) from sys_dummy;
select atan2(cast(0 as char(1)),tan(cast(0 as char(8000)))) from sys_dummy;