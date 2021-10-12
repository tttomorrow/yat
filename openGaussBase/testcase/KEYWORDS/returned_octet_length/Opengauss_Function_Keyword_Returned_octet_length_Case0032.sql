--  @testpoint:opengauss关键字returned_octet_length(非保留)，作为用户名

--关键字returned_octet_length作为用户名不带引号，创建成功
drop user if exists returned_octet_length;
CREATE USER returned_octet_length PASSWORD 'Bigdata@123';
drop user returned_octet_length;

--关键字returned_octet_length作为用户名加双引号，创建成功
drop user if exists "returned_octet_length";
CREATE USER "returned_octet_length" PASSWORD 'Bigdata@123';
drop user "returned_octet_length";
 
--关键字returned_octet_length作为用户名加单引号，合理报错
CREATE USER 'returned_octet_length' PASSWORD 'Bigdata@123';

--关键字returned_octet_length作为用户名加反引号，合理报错
CREATE USER `returned_octet_length` PASSWORD 'Bigdata@123';
