--  @testpoint:openGauss保留关键字unique作为 用户名，不带引号，合理报错
 CREATE USER unique PASSWORD 'Bigdata@123';

 --openGauss保留关键字unique作为 用户名，加双引号，创建成功
 drop user if exists "unique";
 CREATE USER "unique" PASSWORD 'Bigdata@123';
 drop user "unique";
  --openGauss保留关键字unique作为 用户名，加单引号，合理报错
  CREATE USER 'unique' PASSWORD 'Bigdata@123';
  ------openGauss保留关键字unique作为 用户名，加反引号，合理报错
  CREATE USER `unique` PASSWORD 'Bigdata@123';