-- @testpoint: 修改角色权限
drop ROLE if exists miriam;
create ROLE miriam with SYSADMIN IDENTIFIED BY 'Bigdata@123' ;
ALTER ROLE miriam  WITH AUDITADMIN;
drop ROLE if exists miriam;
