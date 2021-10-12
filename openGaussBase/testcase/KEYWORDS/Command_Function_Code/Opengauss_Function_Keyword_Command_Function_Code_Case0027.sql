--  @testpoint:opengauss关键字command_function_code(非保留)，作为序列名


--关键字不带引号-成功
drop sequence if exists command_function_code;
create sequence command_function_code start 100 cache 50;
drop sequence command_function_code;

--关键字带双引号-成功
drop sequence if exists "command_function_code";
create sequence "command_function_code" start 100 cache 50;
drop sequence "command_function_code";

--关键字带单引号-合理报错
drop sequence if exists 'command_function_code';
create sequence 'command_function_code' start 100 cache 50;

--关键字带反引号-合理报错
drop sequence if exists `command_function_code`;
create sequence `command_function_code` start 100 cache 50;
