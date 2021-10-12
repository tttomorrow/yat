--  @testpoint:opengauss关键字K(非保留)，作为用户名

--关键字explain作为用户名不带引号，创建成功
drop user if exists K;
CREATE USER K PASSWORD 'Bigdata@123';
drop user K;

--关键字explain作为用户名加双引号，创建成功
drop user if exists "K";
CREATE USER "K" PASSWORD 'Bigdata@123';
drop user "K";
 
--关键字explain作为用户名加单引号，合理报错
CREATE USER 'K' PASSWORD 'Bigdata@123';

--关键字explain作为用户名加反引号，合理报错
CREATE USER `K` PASSWORD 'Bigdata@123';
