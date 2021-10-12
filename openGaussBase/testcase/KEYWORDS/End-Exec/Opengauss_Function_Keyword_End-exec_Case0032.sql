--  @testpoint:opengauss关键字end-exec(非保留)，作为用户名

--关键字end-exec作为用户名不带引号，创建成功
drop user if exists end-exec;
CREATE USER end-exec PASSWORD 'Bigdata@123';
drop user end-exec;

--关键字end-exec作为用户名加双引号，创建成功
drop user if exists "end-exec";
CREATE USER "end-exec" PASSWORD 'Bigdata@123';
drop user "end-exec";
 
--关键字end-exec作为用户名加单引号，合理报错
CREATE USER 'end-exec' PASSWORD 'Bigdata@123';

--关键字end-exec作为用户名加反引号，合理报错
CREATE USER `end-exec` PASSWORD 'Bigdata@123';
