-- @testpoint: 输入参数为null和''


select bitand(null,3) as result from sys_dummy;
select bitand(6,'') as result from sys_dummy;
select bitand(null,'') as result from sys_dummy;

