-- @testpoint: 修改指定数据库，用户，会话级别的参数listen_addresses，合理报错
-- 修改指定数据库listen_addresses为"55.77.88.99"
alter database postgres set listen_addresses to '55.66.77.88';
-- 修改指定用户listen_addresses为"55.77.88.99"
create user openGauss identified by 'OpenGauss123';
alter user openGauss set listen_addresses to '55.66.77.88';
-- 修改会话级别的listen_addresses为"55.77.88.99"
set listen_addresses to '55.66.77.88';
-- 删除用户
drop user openGauss;