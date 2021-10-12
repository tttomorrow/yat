-- @testpoint: mod函数入参为null/''的测试
select mod(null,null) from sys_dummy;
select mod('','') from sys_dummy;
select mod(null,0) from sys_dummy;
select mod(0,null) from sys_dummy;
select mod(null,'') from sys_dummy;
select mod('',null) from sys_dummy;