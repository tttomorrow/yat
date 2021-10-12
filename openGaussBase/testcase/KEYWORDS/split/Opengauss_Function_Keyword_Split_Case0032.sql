--  @testpoint:openGauss保留关键字split作为用户名

--不带引号，成功
CREATE USER split PASSWORD 'Bigdata@123';

--openGauss保留关键字split作为 用户名，加双引号，创建成功
drop user if exists "split";
CREATE USER "split" PASSWORD 'Bigdata@123';
drop user "split";

--openGauss保留关键字split作为 用户名，加单引号，合理报错
CREATE USER 'split' PASSWORD 'Bigdata@123';

--openGauss保留关键字split作为 用户名，加反引号，合理报错
CREATE USER `split` PASSWORD 'Bigdata@123';