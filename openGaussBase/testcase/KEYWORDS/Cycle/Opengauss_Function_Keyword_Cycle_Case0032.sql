--  @testpoint:opengauss关键字cycle(非保留)，作为用户名

--关键字cycle作为用户名不带引号，创建成功
drop user if exists cycle;
CREATE USER cycle PASSWORD 'Bigdata@123';
drop user cycle;

--关键字cycle作为用户名加双引号，创建成功
drop user if exists "cycle";
CREATE USER "cycle" PASSWORD 'Bigdata@123';
drop user "cycle";
 
--关键字cycle作为用户名加单引号，合理报错
CREATE USER 'cycle' PASSWORD 'Bigdata@123';

--关键字cycle作为用户名加反引号，合理报错
CREATE USER `cycle` PASSWORD 'Bigdata@123';
