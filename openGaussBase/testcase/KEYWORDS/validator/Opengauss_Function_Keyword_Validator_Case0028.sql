-- @testpoint: opengauss关键字validator(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists validator;
create synonym validator for explain_test;
insert into validator values (1,'ada'),(2, 'bob');
update validator set validator.name='cici' where validator.id=2;
select * from validator;
drop synonym if exists validator;

--关键字带双引号-成功
drop synonym if exists "validator";
create synonym "validator" for explain_test;
drop synonym if exists "validator";

--关键字带单引号-合理报错
drop synonym if exists 'validator';
create synonym 'validator' for explain_test;
insert into 'validator' values (1,'ada'),(2, 'bob');
update 'validator' set 'validator'.name='cici' where 'validator'.id=2;
select * from 'validator';

--关键字带反引号-合理报错
drop synonym if exists `validator`;
create synonym `validator` for explain_test;
insert into `validator` values (1,'ada'),(2, 'bob');
update `validator` set `validator`.name='cici' where `validator`.id=2;
select * from `validator`;
drop table if exists explain_test;