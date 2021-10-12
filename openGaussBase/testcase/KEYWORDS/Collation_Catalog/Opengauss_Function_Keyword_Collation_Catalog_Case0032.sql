--  @testpoint:opengauss关键字collation_catalog(非保留)，作为用户名

--关键字collation_catalog作为用户名不带引号，创建成功
drop user if exists collation_catalog;
CREATE USER collation_catalog PASSWORD 'Bigdata@123';
drop user collation_catalog;

--关键字collation_catalog作为用户名加双引号，创建成功
drop user if exists "collation_catalog";
CREATE USER "collation_catalog" PASSWORD 'Bigdata@123';
drop user "collation_catalog";
 
--关键字collation_catalog作为用户名加单引号，合理报错
CREATE USER 'collation_catalog' PASSWORD 'Bigdata@123';

--关键字collation_catalog作为用户名加反引号，合理报错
CREATE USER `collation_catalog` PASSWORD 'Bigdata@123';
