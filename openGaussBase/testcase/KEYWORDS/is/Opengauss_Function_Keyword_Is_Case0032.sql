--  @testpoint:openGauss保留关键字is作为 用户名，

--不带引号，合理报错
 CREATE USER is PASSWORD 'Bigdata@123';

 --加双引号，创建成功
 drop user if exists "is";
 CREATE USER "is" PASSWORD 'Bigdata@123';
 
 --清理环境
 drop user "is";
 
 --加单引号，合理报错
 CREATE USER 'is' PASSWORD 'Bigdata@123';
  
 --加反引号，合理报错
 CREATE USER `is` PASSWORD 'Bigdata@123';