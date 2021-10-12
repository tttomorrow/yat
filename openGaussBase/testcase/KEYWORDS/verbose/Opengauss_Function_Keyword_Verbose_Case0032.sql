-- @testpoint: openGauss保留关键字verbose作为 用户名，合理报错

--不带引号，合理报错
 CREATE USER verbose PASSWORD 'Bigdata@123';

 --加双引号，创建成功
 drop user if exists "verbose";
 CREATE USER "verbose" PASSWORD 'Bigdata@123';
 
 --清理环境
 drop user "verbose";
 
 --加单引号，合理报错
 CREATE USER 'verbose' PASSWORD 'Bigdata@123';
  
 --加反引号，合理报错
 CREATE USER `verbose` PASSWORD 'Bigdata@123';