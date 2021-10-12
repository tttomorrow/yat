--  @testpoint:opengauss关键字raw(非保留)，作为用户名

--关键字raw作为用户名不带引号，创建成功
drop user if exists raw;
CREATE USER raw PASSWORD 'Bigdata@123';
drop user raw;

--关键字raw作为用户名加双引号，创建成功
drop user if exists "raw";
CREATE USER "raw" PASSWORD 'Bigdata@123';
drop user "raw";
 
--关键字raw作为用户名加单引号，合理报错
CREATE USER 'raw' PASSWORD 'Bigdata@123';

--关键字raw作为用户名加反引号，合理报错
CREATE USER `raw` PASSWORD 'Bigdata@123';
