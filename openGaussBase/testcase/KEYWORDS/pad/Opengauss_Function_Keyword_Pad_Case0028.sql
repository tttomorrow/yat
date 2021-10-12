-- @testpoint: opengauss关键字pad(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists pad;
create synonym pad for explain_test;
insert into pad values (1,'ada'),(2, 'bob');
update pad set pad.name='cici' where pad.id=2;
select * from pad;

--关键字带双引号-成功
drop synonym if exists "pad";
create synonym "pad" for explain_test;


--关键字带单引号-合理报错
drop synonym if exists 'pad';
create synonym 'pad' for explain_test;
insert into 'pad' values (1,'ada'),(2, 'bob');
update 'pad' set 'pad'.name='cici' where 'pad'.id=2;
select * from 'pad';

--关键字带反引号-合理报错
drop synonym if exists `pad`;
create synonym `pad` for explain_test;
insert into `pad` values (1,'ada'),(2, 'bob');
update `pad` set `pad`.name='cici' where `pad`.id=2;
select * from `pad`;
--清理环境
drop synonym if exists "pad";
drop synonym if exists pad;
drop table if exists explain_test;