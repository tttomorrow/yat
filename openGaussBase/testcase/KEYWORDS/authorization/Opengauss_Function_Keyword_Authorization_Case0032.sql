--  @testpoint:openGauss保留关键字Authorization作为 用户名，

--不带引号，合理报错
 CREATE USER Authorization PASSWORD 'Bigdata@123';

 --加双引号，创建成功
 drop user if exists "Authorization";
 CREATE USER "Authorization" PASSWORD 'Bigdata@123';
 
 --清理环境
 drop user "Authorization";
 
 --加单引号，合理报错
 CREATE USER 'Authorization' PASSWORD 'Bigdata@123';
  
 --加反引号，合理报错
 CREATE USER `Authorization` PASSWORD 'Bigdata@123';