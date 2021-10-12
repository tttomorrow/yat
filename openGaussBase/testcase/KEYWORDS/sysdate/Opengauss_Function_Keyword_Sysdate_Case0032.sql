--  @testpoint:openGauss保留关键字sysdate作为用户名

--不带引号，合理报错
CREATE USER sysdate PASSWORD 'Bigdata@123';

--openGauss保留关键字sysdate作为 用户名，加双引号，创建成功
drop user if exists "sysdate";
CREATE USER "sysdate" PASSWORD 'Bigdata@123';
drop user "sysdate";

--openGauss保留关键字sysdate作为 用户名，加单引号，合理报错
CREATE USER 'sysdate' PASSWORD 'Bigdata@123';

--openGauss保留关键字sysdate作为 用户名，加反引号，合理报错
CREATE USER `sysdate` PASSWORD 'Bigdata@123';