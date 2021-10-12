--  @testpoint:opengauss关键字constraints(非保留)，作为用户名

--关键字constraints作为用户名不带引号，创建成功
drop user if exists constraints;
CREATE USER constraints PASSWORD 'Bigdata@123';
drop user constraints;

--关键字constraints作为用户名加双引号，创建成功
drop user if exists "constraints";
CREATE USER "constraints" PASSWORD 'Bigdata@123';
drop user "constraints";
 
--关键字constraints作为用户名加单引号，合理报错
CREATE USER 'constraints' PASSWORD 'Bigdata@123';

--关键字constraints作为用户名加反引号，合理报错
CREATE USER `constraints` PASSWORD 'Bigdata@123';
