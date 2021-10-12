--  @testpoint:opengauss关键字privileges(非保留)，作为用户名

--关键字privileges作为用户名不带引号，创建成功
drop user if exists privileges;
CREATE USER privileges PASSWORD 'Bigdata@123';
drop user privileges;

--关键字privileges作为用户名加双引号，创建成功
drop user if exists "privileges";
CREATE USER "privileges" PASSWORD 'Bigdata@123';
drop user "privileges";
 
--关键字privileges作为用户名加单引号，合理报错
CREATE USER 'privileges' PASSWORD 'Bigdata@123';

--关键字privileges作为用户名加反引号，合理报错
CREATE USER `privileges` PASSWORD 'Bigdata@123';
