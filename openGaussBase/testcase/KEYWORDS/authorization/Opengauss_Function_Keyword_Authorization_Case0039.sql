-- @testpoint: 把当前会话里的会话用户标识和当前用户标识都设置为指定的用户
drop role if exists paul;
CREATE ROLE paul IDENTIFIED BY 'Bigdata@123';
SET SESSION AUTHORIZATION paul password 'Bigdata@123';
SELECT SESSION_USER, CURRENT_USER;
RESET SESSION AUTHORIZATION;
drop role if exists paul;
