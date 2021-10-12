-- @testpoint: opengauss关键字destructor(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists destructor_test;
create table destructor_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists destructor;
create synonym destructor for destructor_test;
insert into destructor values (1,'ada'),(2, 'bob');
update destructor set destructor.name='cici' where destructor.id=2;
select * from destructor;
drop synonym if exists destructor;

--关键字带双引号-成功
drop synonym if exists "destructor";
create synonym "destructor" for destructor_test;
drop synonym if exists "destructor";

--关键字带单引号-合理报错
drop synonym if exists 'destructor';
create synonym 'destructor' for destructor_test;
insert into 'destructor' values (1,'ada'),(2, 'bob');
update 'destructor' set 'destructor'.name='cici' where 'destructor'.id=2;
select * from 'destructor';

--关键字带反引号-合理报错
drop synonym if exists `destructor`;
create synonym `destructor` for destructor_test;
insert into `destructor` values (1,'ada'),(2, 'bob');
update `destructor` set `destructor`.name='cici' where `destructor`.id=2;
select * from `destructor`;
drop table if exists destructor_test;