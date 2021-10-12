--  @testpoint:opengauss关键字connection_name(非保留)，作为用户名

--关键字connection_name作为用户名不带引号，创建成功
drop user if exists connection_name;
CREATE USER connection_name PASSWORD 'Bigdata@123';
drop user connection_name;

--关键字connection_name作为用户名加双引号，创建成功
drop user if exists "connection_name";
CREATE USER "connection_name" PASSWORD 'Bigdata@123';
drop user "connection_name";
 
--关键字connection_name作为用户名加单引号，合理报错
CREATE USER 'connection_name' PASSWORD 'Bigdata@123';

--关键字connection_name作为用户名加反引号，合理报错
CREATE USER `connection_name` PASSWORD 'Bigdata@123';
