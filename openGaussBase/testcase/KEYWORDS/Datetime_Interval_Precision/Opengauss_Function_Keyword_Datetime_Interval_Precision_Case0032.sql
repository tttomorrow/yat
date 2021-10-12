--  @testpoint:opengauss关键字datetime_interval_precision(非保留)，作为用户名

--关键字datetime_interval_precision作为用户名不带引号，创建成功
drop user if exists datetime_interval_precision;
CREATE USER datetime_interval_precision PASSWORD 'Bigdata@123';
drop user datetime_interval_precision;

--关键字datetime_interval_precision作为用户名加双引号，创建成功
drop user if exists "datetime_interval_precision";
CREATE USER "datetime_interval_precision" PASSWORD 'Bigdata@123';
drop user "datetime_interval_precision";
 
--关键字datetime_interval_precision作为用户名加单引号，合理报错
CREATE USER 'datetime_interval_precision' PASSWORD 'Bigdata@123';

--关键字datetime_interval_precision作为用户名加反引号，合理报错
CREATE USER `datetime_interval_precision` PASSWORD 'Bigdata@123';
