--  @testpoint:openGauss保留关键字current_role作为 用户名，

--不带引号，合理报错
 CREATE USER current_role PASSWORD 'Bigdata@123';

 --加双引号，创建成功
 drop user if exists "current_role";
 CREATE USER "current_role" PASSWORD 'Bigdata@123';
 
 --清理环境
 drop user "current_role";
 
 --加单引号，合理报错
 CREATE USER 'current_role' PASSWORD 'Bigdata@123';
  
 --加反引号，合理报错
 CREATE USER `current_role` PASSWORD 'Bigdata@123';