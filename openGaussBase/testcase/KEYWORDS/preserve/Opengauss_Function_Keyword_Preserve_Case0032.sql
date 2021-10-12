--  @testpoint:opengauss关键字preserve(非保留)，作为用户名

--关键字preserve作为用户名不带引号，创建成功
drop user if exists preserve;
CREATE USER preserve PASSWORD 'Bigdata@123';
drop user preserve;

--关键字preserve作为用户名加双引号，创建成功
drop user if exists "preserve";
CREATE USER "preserve" PASSWORD 'Bigdata@123';
drop user "preserve";
 
--关键字preserve作为用户名加单引号，合理报错
CREATE USER 'preserve' PASSWORD 'Bigdata@123';

--关键字preserve作为用户名加反引号，合理报错
CREATE USER `preserve` PASSWORD 'Bigdata@123';
