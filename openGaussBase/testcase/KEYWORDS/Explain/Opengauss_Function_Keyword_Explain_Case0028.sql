-- @testpoint: opengauss关键字explain(非保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists explain;
create synonym explain for explain_test;
insert into explain values (1,'ada'),(2, 'bob');
update explain set explain.name='cici' where explain.id=2;
select * from explain;
drop synonym if exists explain;

--关键字带双引号-成功
drop synonym if exists "explain";
create synonym "explain" for explain_test;
drop synonym if exists "explain";

--关键字带单引号-合理报错
drop synonym if exists 'explain';
create synonym 'explain' for explain_test;
insert into 'explain' values (1,'ada'),(2, 'bob');
update 'explain' set 'explain'.name='cici' where 'explain'.id=2;
select * from 'explain';

--关键字带反引号-合理报错
drop synonym if exists `explain`;
create synonym `explain` for explain_test;
insert into `explain` values (1,'ada'),(2, 'bob');
update `explain` set `explain`.name='cici' where `explain`.id=2;
select * from `explain`;
drop table if exists explain_test;