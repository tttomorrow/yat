-- @testpoint: 创建角色并设置登录密码
drop ROLE if exists manager;
CREATE ROLE manager IDENTIFIED BY 'Bigdata@123';
drop ROLE if exists manager;
