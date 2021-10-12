-- @testpoint: 输入为有效边界值


select atan(cast(1.0E-127 as decimal)),tan(cast(1.0E-128 as decimal)) from sys_dummy;
select atan(cast(0 as char(1))),tan(cast(0 as char(8000)))from sys_dummy;