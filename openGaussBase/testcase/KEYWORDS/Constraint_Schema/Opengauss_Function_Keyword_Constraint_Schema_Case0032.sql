--  @testpoint:opengauss关键字constraint_schema(非保留)，作为用户名

--关键字constraint_schema作为用户名不带引号，创建成功
drop user if exists constraint_schema;
CREATE USER constraint_schema PASSWORD 'Bigdata@123';
drop user constraint_schema;

--关键字constraint_schema作为用户名加双引号，创建成功
drop user if exists "constraint_schema";
CREATE USER "constraint_schema" PASSWORD 'Bigdata@123';
drop user "constraint_schema";
 
--关键字constraint_schema作为用户名加单引号，合理报错
CREATE USER 'constraint_schema' PASSWORD 'Bigdata@123';

--关键字constraint_schema作为用户名加反引号，合理报错
CREATE USER `constraint_schema` PASSWORD 'Bigdata@123';
