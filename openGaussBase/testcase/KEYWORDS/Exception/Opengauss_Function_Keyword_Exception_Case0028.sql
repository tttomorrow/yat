-- @testpoint: opengauss关键字Exception(非保留)，作为同义词对象名 合理报错

--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists Exception;
create synonym Exception for explain_test;
insert into Exception values (1,'ada'),(2, 'bob');
update Exception set Exception.name='cici' where Exception.id=2;
select * from Exception;
drop synonym if exists Exception;

--关键字带双引号-成功
drop synonym if exists "Exception";
create synonym "Exception" for explain_test;
drop synonym if exists "Exception";

--关键字带单引号-合理报错
drop synonym if exists 'Exception';
create synonym 'Exception' for explain_test;
insert into 'Exception' values (1,'ada'),(2, 'bob');
update 'Exception' set 'Exception'.name='cici' where 'Exception'.id=2;
select * from 'Exception';

--关键字带反引号-合理报错
drop synonym if exists `Exception`;
create synonym `Exception` for explain_test;
insert into `Exception` values (1,'ada'),(2, 'bob');
update `Exception` set `Exception`.name='cici' where `Exception`.id=2;
select * from `Exception`;
drop table if exists explain_test;