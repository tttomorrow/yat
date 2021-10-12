-- @testpoint: opengauss关键字Load(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists Load;
create synonym Load for explain_test;
insert into Load values (1,'ada'),(2, 'bob');
update Load set Load.name='cici' where Load.id=2;
select * from Load;

--关键字带双引号-成功
drop synonym if exists "Load";
create synonym "Load" for explain_test;


--关键字带单引号-合理报错
drop synonym if exists 'Load';
create synonym 'Load' for explain_test;
insert into 'Load' values (1,'ada'),(2, 'bob');
update 'Load' set 'Load'.name='cici' where 'Load'.id=2;
select * from 'Load';

--关键字带反引号-合理报错
drop synonym if exists `Load`;
create synonym `Load` for explain_test;
insert into `Load` values (1,'ada'),(2, 'bob');
update `Load` set `Load`.name='cici' where `Load`.id=2;
select * from `Load`;
--清理环境
drop synonym if exists load;
drop synonym if exists "Load";
drop table if exists explain_test;