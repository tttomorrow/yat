--  @testpoint:opengauss关键字before(非保留)，作为用户名
--关键字before作为用户名不带引号，创建成功
drop user if exists before;
CREATE USER before PASSWORD 'Bigdata@123';

--清理环境
drop user before;

--关键字before作为用户名加双引号，创建成功
drop user if exists "before";
CREATE USER "before" PASSWORD 'Bigdata@123';

--清理环境
drop user "before";

--关键字before作为用户名加单引号，合理报错
CREATE USER 'before' PASSWORD 'Bigdata@123';

--关键字before作为用户名加反引号，合理报错
CREATE USER `before` PASSWORD 'Bigdata@123';
