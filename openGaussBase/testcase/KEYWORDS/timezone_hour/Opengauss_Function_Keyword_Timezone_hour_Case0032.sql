--  @testpoint:opengauss关键字timezone_hour(非保留)，作为用户名

--关键字explain作为用户名不带引号，创建成功
drop user if exists timezone_hour;
CREATE USER timezone_hour PASSWORD 'Bigdata@123';
drop user timezone_hour;

--关键字explain作为用户名加双引号，创建成功
drop user if exists "timezone_hour";
CREATE USER "timezone_hour" PASSWORD 'Bigdata@123';
drop user "timezone_hour";
 
--关键字explain作为用户名加单引号，合理报错
CREATE USER 'timezone_hour' PASSWORD 'Bigdata@123';

--关键字explain作为用户名加反引号，合理报错
CREATE USER `timezone_hour` PASSWORD 'Bigdata@123';
