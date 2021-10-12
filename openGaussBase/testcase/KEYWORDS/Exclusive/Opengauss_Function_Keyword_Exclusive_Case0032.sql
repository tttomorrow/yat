--  @testpoint:opengauss关键字exclusive(非保留)，作为用户名

--关键字exclusive作为用户名不带引号，创建成功
drop user if exists exclusive;
CREATE USER exclusive PASSWORD 'Bigdata@123';
drop user exclusive;

--关键字exclusive作为用户名加双引号，创建成功
drop user if exists "exclusive";
CREATE USER "exclusive" PASSWORD 'Bigdata@123';
drop user "exclusive";
 
--关键字exclusive作为用户名加单引号，合理报错
CREATE USER 'exclusive' PASSWORD 'Bigdata@123';

--关键字exclusive作为用户名加反引号，合理报错
CREATE USER `exclusive` PASSWORD 'Bigdata@123';
