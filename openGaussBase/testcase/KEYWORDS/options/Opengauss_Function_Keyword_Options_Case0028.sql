-- @testpoint: opengauss关键字options(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists options;
create synonym options for explain_test;
insert into options values (1,'ada'),(2, 'bob');
update options set options.name='cici' where options.id=2;
select * from options;

--关键字带双引号-成功
drop synonym if exists "options";
create synonym "options" for explain_test;


--关键字带单引号-合理报错
drop synonym if exists 'options';
create synonym 'options' for explain_test;
insert into 'options' values (1,'ada'),(2, 'bob');
update 'options' set 'options'.name='cici' where 'options'.id=2;
select * from 'options';

--关键字带反引号-合理报错
drop synonym if exists `options`;
create synonym `options` for explain_test;
insert into `options` values (1,'ada'),(2, 'bob');
update `options` set `options`.name='cici' where `options`.id=2;
select * from `options`;
--清理环境
drop synonym if exists "options";
drop synonym if exists options;
drop table if exists explain_test;