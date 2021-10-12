-- @testpoint: opengauss关键字only(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-合理报错
drop synonym if exists only;
create synonym only for explain_test;
insert into only values (1,'ada'),(2, 'bob');
update only set only.name='cici' where only.id=2;
select * from only;

--关键字带双引号-成功
drop synonym if exists "only";
create synonym "only" for explain_test;


--关键字带单引号-合理报错
drop synonym if exists 'only';
create synonym 'only' for explain_test;
insert into 'only' values (1,'ada'),(2, 'bob');
update 'only' set 'only'.name='cici' where 'only'.id=2;
select * from 'only';

--关键字带反引号-合理报错
drop synonym if exists `only`;
create synonym `only` for explain_test;
insert into `only` values (1,'ada'),(2, 'bob');
update `only` set `only`.name='cici' where `only`.id=2;
select * from `only`;
--清理环境
drop synonym if exists "only";
drop table if exists explain_test;