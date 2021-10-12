--  @testpoint:opengauss关键字quote(非保留)，作为用户名

--关键字quote作为用户名不带引号，创建成功
drop user if exists quote;
CREATE USER quote PASSWORD 'Bigdata@123';
drop user quote;

--关键字quote作为用户名加双引号，创建成功
drop user if exists "quote";
CREATE USER "quote" PASSWORD 'Bigdata@123';
drop user "quote";
 
--关键字quote作为用户名加单引号，合理报错
CREATE USER 'quote' PASSWORD 'Bigdata@123';

--关键字quote作为用户名加反引号，合理报错
CREATE USER `quote` PASSWORD 'Bigdata@123';
