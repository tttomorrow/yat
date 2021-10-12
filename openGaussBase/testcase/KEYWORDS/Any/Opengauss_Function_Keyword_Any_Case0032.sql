--  @testpoint:openGauss保留关键字Any作为 用户名，

--不带引号，合理报错
 CREATE USER Any PASSWORD 'Bigdata@123';

 --加双引号，创建成功
 drop user if exists "Any";
 CREATE USER "Any" PASSWORD 'Bigdata@123';
 
 --清理环境
 drop user "Any";
 
 --加单引号，合理报错
 CREATE USER 'Any' PASSWORD 'Bigdata@123';
  
 --加反引号，合理报错
 CREATE USER `Any` PASSWORD 'Bigdata@123';