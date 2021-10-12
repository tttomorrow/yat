-- @testpoint: 创建一个是系统管理员的角色
drop ROLE if exists sjk;
create ROLE sjk with SYSADMIN IDENTIFIED BY 'Bigdata@123' ;
drop ROLE if exists sjk;