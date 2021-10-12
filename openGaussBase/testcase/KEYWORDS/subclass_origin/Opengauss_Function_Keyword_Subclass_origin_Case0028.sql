-- @testpoint: opengauss关键字subclass_origin(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists subclass_origin;
create synonym subclass_origin for explain_test;
insert into subclass_origin values (1,'ada'),(2, 'bob');
update subclass_origin set subclass_origin.name='cici' where subclass_origin.id=2;
select * from subclass_origin;
drop synonym if exists subclass_origin;

--关键字带双引号-成功
drop synonym if exists "subclass_origin";
create synonym "subclass_origin" for explain_test;
drop synonym if exists "subclass_origin";

--关键字带单引号-合理报错
drop synonym if exists 'subclass_origin';
create synonym 'subclass_origin' for explain_test;
insert into 'subclass_origin' values (1,'ada'),(2, 'bob');
update 'subclass_origin' set 'subclass_origin'.name='cici' where 'subclass_origin'.id=2;
select * from 'subclass_origin';

--关键字带反引号-合理报错
drop synonym if exists `subclass_origin`;
create synonym `subclass_origin` for explain_test;
insert into `subclass_origin` values (1,'ada'),(2, 'bob');
update `subclass_origin` set `subclass_origin`.name='cici' where `subclass_origin`.id=2;
select * from `subclass_origin`;

--清理环境
drop table if exists explain_test cascade;