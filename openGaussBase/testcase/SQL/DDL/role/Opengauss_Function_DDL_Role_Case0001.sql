-- @testpoint: 创建角色
drop ROLE if exists sys_role;
CREATE  ROLE  sys_role with  createdb IDENTIFIED BY 'Bigdata@123' ;
drop ROLE if exists sys_role;
