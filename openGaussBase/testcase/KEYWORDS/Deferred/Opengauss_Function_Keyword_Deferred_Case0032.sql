--  @testpoint:opengauss关键字deferred(非保留)，作为用户名

--关键字deferred作为用户名不带引号，创建成功
drop user if exists deferred;
CREATE USER deferred PASSWORD 'Bigdata@123';
drop user deferred;

--关键字deferred作为用户名加双引号，创建成功
drop user if exists "deferred";
CREATE USER "deferred" PASSWORD 'Bigdata@123';
drop user "deferred";
 
--关键字deferred作为用户名加单引号，合理报错
CREATE USER 'deferred' PASSWORD 'Bigdata@123';

--关键字deferred作为用户名加反引号，合理报错
CREATE USER `deferred` PASSWORD 'Bigdata@123';
