-- @testpoint: opengauss关键字Key_Type(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists Key_Type;
create synonym Key_Type for explain_test;
insert into Key_Type values (1,'ada'),(2, 'bob');
update Key_Type set Key_Type.name='cici' where Key_Type.id=2;
select * from Key_Type;

--关键字带双引号-成功
drop synonym if exists "Key_Type";
create synonym "Key_Type" for explain_test;


--关键字带单引号-合理报错
drop synonym if exists 'Key_Type';
create synonym 'Key_Type' for explain_test;
insert into 'Key_Type' values (1,'ada'),(2, 'bob');
update 'Key_Type' set 'Key_Type'.name='cici' where 'Key_Type'.id=2;
select * from 'Key_Type';

--关键字带反引号-合理报错
drop synonym if exists `Key_Type`;
create synonym `Key_Type` for explain_test;
insert into `Key_Type` values (1,'ada'),(2, 'bob');
update `Key_Type` set `Key_Type`.name='cici' where `Key_Type`.id=2;
select * from `Key_Type`;
--清理环境
drop synonym if exists key_Type;
drop synonym if exists "Key_Type";
drop table if exists explain_test;