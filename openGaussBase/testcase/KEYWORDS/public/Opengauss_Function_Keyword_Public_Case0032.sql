--  @testpoint:opengauss关键字public(非保留)，作为用户名

--关键字public作为用户名不带引号，合理报错
drop user if exists public;
CREATE USER public PASSWORD 'Bigdata@123';

--关键字public作为用户名加双引号，合理报错
drop user if exists "public";
CREATE USER "public" PASSWORD 'Bigdata@123';
 
--关键字public作为用户名加单引号，合理报错
CREATE USER 'public' PASSWORD 'Bigdata@123';

--关键字public作为用户名加反引号，合理报错
CREATE USER `public` PASSWORD 'Bigdata@123';
