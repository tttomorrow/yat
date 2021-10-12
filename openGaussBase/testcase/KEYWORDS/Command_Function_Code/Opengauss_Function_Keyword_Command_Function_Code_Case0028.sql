-- @testpoint: opengauss关键字command_function_code(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists command_function_code_test;
create table command_function_code_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists command_function_code;
create synonym command_function_code for command_function_code_test;
insert into command_function_code values (1,'ada'),(2, 'bob');
update command_function_code set command_function_code.name='cici' where command_function_code.id=2;
select * from command_function_code;
drop synonym if exists command_function_code;
--关键字带双引号-成功
drop synonym if exists "command_function_code";
create synonym "command_function_code" for command_function_code_test;
drop synonym if exists "command_function_code";

--关键字带单引号-合理报错
drop synonym if exists 'command_function_code';
create synonym 'command_function_code' for command_function_code_test;
insert into 'command_function_code' values (1,'ada'),(2, 'bob');
update 'command_function_code' set 'command_function_code'.name='cici' where 'command_function_code'.id=2;
select * from 'command_function_code';

--关键字带反引号-合理报错
drop synonym if exists `command_function_code`;
create synonym `command_function_code` for command_function_code_test;
insert into `command_function_code` values (1,'ada'),(2, 'bob');
update `command_function_code` set `command_function_code`.name='cici' where `command_function_code`.id=2;
select * from `command_function_code`;
drop table if exists command_function_code_test;