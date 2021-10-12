--  @testpoint:opengauss关键字coalesce(非保留)，作为用户名
--关键字coalesce作为用户名不带引号，创建成功
drop user if exists coalesce;
CREATE USER coalesce PASSWORD 'Bigdata@123';

--清理环境
drop user coalesce;

--关键字coalesce作为用户名加双引号，创建成功
drop user if exists "coalesce";
CREATE USER "coalesce" PASSWORD 'Bigdata@123';

--清理环境
drop user "coalesce";

--关键字coalesce作为用户名加单引号，合理报错
CREATE USER 'coalesce' PASSWORD 'Bigdata@123';

--关键字coalesce作为用户名加反引号，合理报错
CREATE USER `coalesce` PASSWORD 'Bigdata@123';
