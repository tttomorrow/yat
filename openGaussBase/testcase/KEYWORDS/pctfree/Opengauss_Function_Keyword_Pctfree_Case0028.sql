-- @testpoint: opengauss关键字pctfree(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists pctfree;
create synonym pctfree for explain_test;
insert into pctfree values (1,'ada'),(2, 'bob');
update pctfree set pctfree.name='cici' where pctfree.id=2;
select * from pctfree;

--关键字带双引号-成功
drop synonym if exists "pctfree";
create synonym "pctfree" for explain_test;


--关键字带单引号-合理报错
drop synonym if exists 'pctfree';
create synonym 'pctfree' for explain_test;
insert into 'pctfree' values (1,'ada'),(2, 'bob');
update 'pctfree' set 'pctfree'.name='cici' where 'pctfree'.id=2;
select * from 'pctfree';

--关键字带反引号-合理报错
drop synonym if exists `pctfree`;
create synonym `pctfree` for explain_test;
insert into `pctfree` values (1,'ada'),(2, 'bob');
update `pctfree` set `pctfree`.name='cici' where `pctfree`.id=2;
select * from `pctfree`;
--清理环境
drop synonym if exists "pctfree";
drop synonym if exists pctfree;
drop table if exists explain_test;