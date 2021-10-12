--  @testpoint:opengauss关键字cascaded(非保留)，作为用户名
--关键字cascaded作为用户名不带引号，创建成功
drop user if exists cascaded;
CREATE USER cascaded PASSWORD 'Bigdata@123';

--清理环境
drop user cascaded;

--关键字cascaded作为用户名加双引号，创建成功
drop user if exists "cascaded";
CREATE USER "cascaded" PASSWORD 'Bigdata@123';

--清理环境
drop user "cascaded";

--关键字cascaded作为用户名加单引号，合理报错
CREATE USER 'cascaded' PASSWORD 'Bigdata@123';

--关键字cascaded作为用户名加反引号，合理报错
CREATE USER `cascaded` PASSWORD 'Bigdata@123';
