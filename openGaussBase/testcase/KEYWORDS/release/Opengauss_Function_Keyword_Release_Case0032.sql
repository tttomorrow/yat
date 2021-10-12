--  @testpoint:opengauss关键字release(非保留)，作为用户名

--关键字release作为用户名不带引号，创建成功
drop user if exists release;
CREATE USER release PASSWORD 'Bigdata@123';
drop user release;

--关键字release作为用户名加双引号，创建成功
drop user if exists "release";
CREATE USER "release" PASSWORD 'Bigdata@123';
drop user "release";
 
--关键字release作为用户名加单引号，合理报错
CREATE USER 'release' PASSWORD 'Bigdata@123';

--关键字release作为用户名加反引号，合理报错
CREATE USER `release` PASSWORD 'Bigdata@123';
