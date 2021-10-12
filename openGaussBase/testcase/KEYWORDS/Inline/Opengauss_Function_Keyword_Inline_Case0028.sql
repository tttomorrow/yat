-- @testpoint: opengauss关键字Inline(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists Inline;
create synonym Inline for explain_test;
insert into Inline values (1,'ada'),(2, 'bob');
update Inline set Inline.name='cici' where Inline.id=2;
select * from Inline;

--关键字带双引号-成功
drop synonym if exists "Inline";
create synonym "Inline" for explain_test;


--关键字带单引号-合理报错
drop synonym if exists 'Inline';
create synonym 'Inline' for explain_test;
insert into 'Inline' values (1,'ada'),(2, 'bob');
update 'Inline' set 'Inline'.name='cici' where 'Inline'.id=2;
select * from 'Inline';

--关键字带反引号-合理报错
drop synonym if exists `Inline`;
create synonym `Inline` for explain_test;
insert into `Inline` values (1,'ada'),(2, 'bob');
update `Inline` set `Inline`.name='cici' where `Inline`.id=2;
select * from `Inline`;
--清理环境
drop synonym if exists inline;
drop synonym if exists "Inline";
drop table if exists explain_test;