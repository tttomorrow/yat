--  @testpoint:opengauss关键字command_function_code(非保留)，作为用户名


--关键字command_function_code作为视图名，不带引号，创建成功
CREATE or replace VIEW command_function_code AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

--关键字command_function_code作为视图名，加双引号，创建成功
CREATE  or replace VIEW "command_function_code" AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
drop VIEW "command_function_code";

--关键字command_function_code作为视图名，加单引号，合理报错
CREATE or replace VIEW 'command_function_code' AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

--关键字command_function_code作为视图名，加反引号，合理报错
CREATE or replace VIEW `command_function_code` AS
SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

