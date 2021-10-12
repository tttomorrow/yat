--  @testpoint:opengauss关键字following(非保留)，作为用户名

--关键字following作为用户名不带引号，创建成功
drop user if exists following;
CREATE USER following PASSWORD 'Bigdata@123';
drop user following;

--关键字following作为用户名加双引号，创建成功
drop user if exists "following";
CREATE USER "following" PASSWORD 'Bigdata@123';
drop user "following";
 
--关键字following作为用户名加单引号，合理报错
CREATE USER 'following' PASSWORD 'Bigdata@123';

--关键字following作为用户名加反引号，合理报错
CREATE USER `following` PASSWORD 'Bigdata@123';
