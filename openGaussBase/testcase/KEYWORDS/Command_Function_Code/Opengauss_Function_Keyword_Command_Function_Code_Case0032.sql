--  @testpoint:opengauss关键字command_function_code(非保留)，作为用户名

--关键字command_function_code作为用户名不带引号，创建成功
drop user if exists command_function_code;
CREATE USER command_function_code PASSWORD 'Bigdata@123';
drop user command_function_code;

--关键字command_function_code作为用户名加双引号，创建成功
drop user if exists "command_function_code";
CREATE USER "command_function_code" PASSWORD 'Bigdata@123';
drop user "command_function_code";
 
--关键字command_function_code作为用户名加单引号，合理报错
CREATE USER 'command_function_code' PASSWORD 'Bigdata@123';

--关键字command_function_code作为用户名加反引号，合理报错
CREATE USER `command_function_code` PASSWORD 'Bigdata@123';
