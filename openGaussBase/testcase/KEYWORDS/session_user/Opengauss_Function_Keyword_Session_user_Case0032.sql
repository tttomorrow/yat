--  @testpoint:openGauss保留关键字session_user作为 用户名，

--不带引号，合理报错
 CREATE USER session_user PASSWORD 'Bigdata@123';

 --加双引号，创建成功
 drop user if exists "session_user";
 CREATE USER "session_user" PASSWORD 'Bigdata@123';
 
 --清理环境
 drop user "session_user";
 
 --加单引号，合理报错
 CREATE USER 'session_user' PASSWORD 'Bigdata@123';
  
 --加反引号，合理报错
 CREATE USER `session_user` PASSWORD 'Bigdata@123';