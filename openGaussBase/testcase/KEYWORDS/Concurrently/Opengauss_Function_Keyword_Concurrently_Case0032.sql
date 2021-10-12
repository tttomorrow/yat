--  @testpoint:opengauss关键字concurrently(非保留)，作为用户名

--关键字concurrently作为用户名不带引号，创建成功
drop user if exists concurrently;
CREATE USER concurrently PASSWORD 'Bigdata@123';
drop user concurrently;

--关键字concurrently作为用户名加双引号，创建成功
drop user if exists "concurrently";
CREATE USER "concurrently" PASSWORD 'Bigdata@123';
drop user "concurrently";
 
--关键字concurrently作为用户名加单引号，合理报错
CREATE USER 'concurrently' PASSWORD 'Bigdata@123';

--关键字concurrently作为用户名加反引号，合理报错
CREATE USER `concurrently` PASSWORD 'Bigdata@123';
