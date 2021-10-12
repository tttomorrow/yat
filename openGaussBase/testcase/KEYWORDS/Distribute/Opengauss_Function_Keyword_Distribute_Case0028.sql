-- @testpoint: opengauss关键字distribute(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists distribute_test;
create table distribute_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists distribute;
create synonym distribute for distribute_test;
insert into distribute values (1,'ada'),(2, 'bob');
update distribute set distribute.name='cici' where distribute.id=2;
select * from distribute;
drop synonym if exists distribute;

--关键字带双引号-成功
drop synonym if exists "distribute";
create synonym "distribute" for distribute_test;
drop synonym if exists "distribute";

--关键字带单引号-合理报错
drop synonym if exists 'distribute';
create synonym 'distribute' for distribute_test;
insert into 'distribute' values (1,'ada'),(2, 'bob');
update 'distribute' set 'distribute'.name='cici' where 'distribute'.id=2;
select * from 'distribute';

--关键字带反引号-合理报错
drop synonym if exists `distribute`;
create synonym `distribute` for distribute_test;
insert into `distribute` values (1,'ada'),(2, 'bob');
update `distribute` set `distribute`.name='cici' where `distribute`.id=2;
select * from `distribute`;
drop table if exists distribute_test;