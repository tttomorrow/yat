--  @testpoint:opengauss关键字reloptions(非保留)，作为用户名

--关键字reloptions作为用户名不带引号，创建成功
drop user if exists reloptions;
CREATE USER reloptions PASSWORD 'Bigdata@123';
drop user reloptions;

--关键字reloptions作为用户名加双引号，创建成功
drop user if exists "reloptions";
CREATE USER "reloptions" PASSWORD 'Bigdata@123';
drop user "reloptions";
 
--关键字reloptions作为用户名加单引号，合理报错
CREATE USER 'reloptions' PASSWORD 'Bigdata@123';

--关键字reloptions作为用户名加反引号，合理报错
CREATE USER `reloptions` PASSWORD 'Bigdata@123';
