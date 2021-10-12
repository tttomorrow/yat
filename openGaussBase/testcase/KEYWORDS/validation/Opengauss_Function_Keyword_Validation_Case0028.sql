-- @testpoint: opengauss关键字validation(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists validation;
create synonym validation for explain_test;
insert into validation values (1,'ada'),(2, 'bob');
update validation set validation.name='cici' where validation.id=2;
select * from validation;
drop synonym if exists validation;

--关键字带双引号-成功
drop synonym if exists "validation";
create synonym "validation" for explain_test;
drop synonym if exists "validation";

--关键字带单引号-合理报错
drop synonym if exists 'validation';
create synonym 'validation' for explain_test;
insert into 'validation' values (1,'ada'),(2, 'bob');
update 'validation' set 'validation'.name='cici' where 'validation'.id=2;
select * from 'validation';

--关键字带反引号-合理报错
drop synonym if exists `validation`;
create synonym `validation` for explain_test;
insert into `validation` values (1,'ada'),(2, 'bob');
update `validation` set `validation`.name='cici' where `validation`.id=2;
select * from `validation`;
drop table if exists explain_test;