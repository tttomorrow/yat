--  @testpoint:opengauss关键字comment(非保留)，作为用户名

--关键字comment作为用户名不带引号，创建成功
drop user if exists comment;
CREATE USER comment PASSWORD 'Bigdata@123';
drop user comment;

--关键字comment作为用户名加双引号，创建成功
drop user if exists "comment";
CREATE USER "comment" PASSWORD 'Bigdata@123';
drop user "comment";
 
--关键字comment作为用户名加单引号，合理报错
CREATE USER 'comment' PASSWORD 'Bigdata@123';

--关键字comment作为用户名加反引号，合理报错
CREATE USER `comment` PASSWORD 'Bigdata@123';
