--  @testpoint:opengauss关键字prepare(非保留)，作为用户名

--关键字prepare作为用户名不带引号，创建成功
drop user if exists prepare;
CREATE USER prepare PASSWORD 'Bigdata@123';
drop user prepare;

--关键字prepare作为用户名加双引号，创建成功
drop user if exists "prepare";
CREATE USER "prepare" PASSWORD 'Bigdata@123';
drop user "prepare";
 
--关键字prepare作为用户名加单引号，合理报错
CREATE USER 'prepare' PASSWORD 'Bigdata@123';

--关键字prepare作为用户名加反引号，合理报错
CREATE USER `prepare` PASSWORD 'Bigdata@123';
