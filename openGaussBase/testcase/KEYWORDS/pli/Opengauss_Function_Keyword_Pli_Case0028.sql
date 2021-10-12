-- @testpoint: opengauss关键字pli(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists pli_test;
create table pli_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists pli;
create synonym pli for pli_test;
insert into pli values (1,'ada'),(2, 'bob');
update pli set pli.name='cici' where pli.id=2;
select * from pli;

--关键字带双引号-成功
drop synonym if exists "pli";
create synonym "pli" for pli_test;


--关键字带单引号-合理报错
drop synonym if exists 'pli';
create synonym 'pli' for pli_test;
insert into 'pli' values (1,'ada'),(2, 'bob');
update 'pli' set 'pli'.name='cici' where 'pli'.id=2;
select * from 'pli';

--关键字带反引号-合理报错
drop synonym if exists `pli`;
create synonym `pli` for pli_test;
insert into `pli` values (1,'ada'),(2, 'bob');
update `pli` set `pli`.name='cici' where `pli`.id=2;
select * from `pli`;
--清理环境
drop synonym if exists "pli";
drop synonym if exists pli;
drop table if exists pli_test;