--  @testpoint:opengauss关键字type(非保留)，作为用户名

--关键字explain作为用户名不带引号，创建成功
drop user if exists type;
CREATE USER type PASSWORD 'Bigdata@123';
drop user type;

--关键字explain作为用户名加双引号，创建成功
drop user if exists "type";
CREATE USER "type" PASSWORD 'Bigdata@123';
drop user "type";
 
--关键字explain作为用户名加单引号，合理报错
CREATE USER 'type' PASSWORD 'Bigdata@123';

--关键字explain作为用户名加反引号，合理报错
CREATE USER `type` PASSWORD 'Bigdata@123';
