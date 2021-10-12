--  @testpoint:opengauss关键字binary_double(非保留)，作为用户名
--关键字binary_double作为用户名不带引号，创建成功
drop user if exists binary_double;
CREATE USER binary_double PASSWORD 'Bigdata@123';

--清理环境
drop user binary_double;

--关键字binary_double作为用户名加双引号，创建成功
drop user if exists "binary_double";
CREATE USER "binary_double" PASSWORD 'Bigdata@123';

--清理环境
drop user "binary_double";

--关键字binary_double作为用户名加单引号，合理报错
CREATE USER 'binary_double' PASSWORD 'Bigdata@123';

--关键字binary_double作为用户名加反引号，合理报错
CREATE USER `binary_double` PASSWORD 'Bigdata@123';
