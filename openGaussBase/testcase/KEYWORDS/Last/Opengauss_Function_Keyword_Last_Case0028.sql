-- @testpoint: opengauss关键字Last(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists Last;
create synonym Last for explain_test;
insert into Last values (1,'ada'),(2, 'bob');
update Last set Last.name='cici' where Last.id=2;
select * from Last;

--关键字带双引号-成功
drop synonym if exists "Last";
create synonym "Last" for explain_test;


--关键字带单引号-合理报错
drop synonym if exists 'Last';
create synonym 'Last' for explain_test;
insert into 'Last' values (1,'ada'),(2, 'bob');
update 'Last' set 'Last'.name='cici' where 'Last'.id=2;
select * from 'Last';

--关键字带反引号-合理报错
drop synonym if exists `Last`;
create synonym `Last` for explain_test;
insert into `Last` values (1,'ada'),(2, 'bob');
update `Last` set `Last`.name='cici' where `Last`.id=2;
select * from `Last`;
--清理环境
drop synonym if exists last;
drop synonym if exists "Last";
drop table if exists explain_test;