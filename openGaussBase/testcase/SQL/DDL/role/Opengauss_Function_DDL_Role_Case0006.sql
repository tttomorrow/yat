-- @testpoint: 修改角色名称
drop ROLE if exists sys_role;
create ROLE sys_role with SYSADMIN IDENTIFIED BY 'Bigdata@123' ;
DROP ROLE if exists jim;
ALTER ROLE sys_role RENAME TO jim;
DROP ROLE if exists jim;