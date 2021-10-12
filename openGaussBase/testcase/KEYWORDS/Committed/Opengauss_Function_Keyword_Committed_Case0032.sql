--  @testpoint:opengauss关键字committed(非保留)，作为用户名

--关键字committed作为用户名不带引号，创建成功
drop user if exists committed;
CREATE USER committed PASSWORD 'Bigdata@123';
drop user committed;

--关键字committed作为用户名加双引号，创建成功
drop user if exists "committed";
CREATE USER "committed" PASSWORD 'Bigdata@123';
drop user "committed";
 
--关键字committed作为用户名加单引号，合理报错
CREATE USER 'committed' PASSWORD 'Bigdata@123';

--关键字committed作为用户名加反引号，合理报错
CREATE USER `committed` PASSWORD 'Bigdata@123';
