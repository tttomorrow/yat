-- @testpoint: opengauss关键字datetime_interval_code(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists datetime_interval_code_test;
create table datetime_interval_code_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists datetime_interval_code;
create synonym datetime_interval_code for datetime_interval_code_test;
insert into datetime_interval_code values (1,'ada'),(2, 'bob');
update datetime_interval_code set datetime_interval_code.name='cici' where datetime_interval_code.id=2;
select * from datetime_interval_code;
drop synonym if exists datetime_interval_code;

--关键字带双引号-成功
drop synonym if exists "datetime_interval_code";
create synonym "datetime_interval_code" for datetime_interval_code_test;
drop synonym if exists "datetime_interval_code";

--关键字带单引号-合理报错
drop synonym if exists 'datetime_interval_code';
create synonym 'datetime_interval_code' for datetime_interval_code_test;
insert into 'datetime_interval_code' values (1,'ada'),(2, 'bob');
update 'datetime_interval_code' set 'datetime_interval_code'.name='cici' where 'datetime_interval_code'.id=2;
select * from 'datetime_interval_code';

--关键字带反引号-合理报错
drop synonym if exists `datetime_interval_code`;
create synonym `datetime_interval_code` for datetime_interval_code_test;
insert into `datetime_interval_code` values (1,'ada'),(2, 'bob');
update `datetime_interval_code` set `datetime_interval_code`.name='cici' where `datetime_interval_code`.id=2;
select * from `datetime_interval_code`;
drop table if exists datetime_interval_code_test;