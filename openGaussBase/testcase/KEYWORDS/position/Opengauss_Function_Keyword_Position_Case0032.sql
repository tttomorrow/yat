--  @testpoint:opengauss关键字position(非保留)，作为用户名

--关键字position作为用户名不带引号，创建成功
drop user if exists position;
CREATE USER position PASSWORD 'Bigdata@123';
drop user position;

--关键字position作为用户名加双引号，创建成功
drop user if exists "position";
CREATE USER "position" PASSWORD 'Bigdata@123';
drop user "position";
 
--关键字position作为用户名加单引号，合理报错
CREATE USER 'position' PASSWORD 'Bigdata@123';

--关键字position作为用户名加反引号，合理报错
CREATE USER `position` PASSWORD 'Bigdata@123';
