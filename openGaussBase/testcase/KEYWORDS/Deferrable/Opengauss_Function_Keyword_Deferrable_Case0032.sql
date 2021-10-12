--  @testpoint:openGauss保留关键字deferrable作为 用户名，不带引号，合理报错
 CREATE USER deferrable PASSWORD 'Bigdata@123';

 --openGauss保留关键字deferrable作为 用户名，加双引号，创建成功
 drop user if exists "deferrable";
 CREATE USER "deferrable" PASSWORD 'Bigdata@123';
 drop user "deferrable";
  --openGauss保留关键字deferrable作为 用户名，加单引号，合理报错
  CREATE USER 'deferrable' PASSWORD 'Bigdata@123';
  ------openGauss保留关键字deferrable作为 用户名，加反引号，合理报错
  CREATE USER `deferrable` PASSWORD 'Bigdata@123';