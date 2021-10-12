-- @testpoint: 修改XX角色 为系统管理员
drop ROLE if exists sjk;
create ROLE sjk with SYSADMIN IDENTIFIED BY 'Bigdata@123' ;
ALTER ROLE sjk SYSADMIN;
drop ROLE if exists sjk;
