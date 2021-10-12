--  @testpoint:opengauss关键字mode(非保留)，作为用户名

--关键字explain作为用户名不带引号，创建成功
drop user if exists mode;
CREATE USER mode PASSWORD 'Bigdata@123';
drop user mode;

--关键字explain作为用户名加双引号，创建成功
drop user if exists "mode";
CREATE USER "mode" PASSWORD 'Bigdata@123';
drop user "mode";
 
--关键字explain作为用户名加单引号，合理报错
CREATE USER 'mode' PASSWORD 'Bigdata@123';

--关键字explain作为用户名加反引号，合理报错
CREATE USER `mode` PASSWORD 'Bigdata@123';
