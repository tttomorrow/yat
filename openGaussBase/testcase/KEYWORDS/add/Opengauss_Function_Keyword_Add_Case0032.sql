--  @testpoint:opengauss关键字add(非保留)，作为用户名
--关键字add作为用户名不带引号，创建成功
drop user if exists add;
CREATE USER add PASSWORD 'Bigdata@123';

--清理环境
drop user add;

--关键字add作为用户名加双引号，创建成功
drop user if exists "add";
CREATE USER "add" PASSWORD 'Bigdata@123';

--清理环境
drop user "add";

--关键字add作为用户名加单引号，合理报错
CREATE USER 'add' PASSWORD 'Bigdata@123';

--关键字add作为用户名加反引号，合理报错
CREATE USER `add` PASSWORD 'Bigdata@123';
