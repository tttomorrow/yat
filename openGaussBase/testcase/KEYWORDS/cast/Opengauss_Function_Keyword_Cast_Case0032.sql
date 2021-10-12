--  @testpoint:openGauss保留关键字Cast作为 用户名，

--不带引号，合理报错
 CREATE USER Cast PASSWORD 'Bigdata@123';

 --加双引号，创建成功
 drop user if exists "Cast";
 CREATE USER "Cast" PASSWORD 'Bigdata@123';
 
 --清理环境
 drop user "Cast";
 
 --加单引号，合理报错
 CREATE USER 'Cast' PASSWORD 'Bigdata@123';
  
 --加反引号，合理报错
 CREATE USER `Cast` PASSWORD 'Bigdata@123';