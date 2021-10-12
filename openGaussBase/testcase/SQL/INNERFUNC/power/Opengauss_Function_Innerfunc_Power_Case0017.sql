-- @testpoint: power函数,俩参数同时为0、null、''
select power(0,0) as result from sys_dummy;
select power(null,null) as result from sys_dummy;
select power('','') as result from sys_dummy;
