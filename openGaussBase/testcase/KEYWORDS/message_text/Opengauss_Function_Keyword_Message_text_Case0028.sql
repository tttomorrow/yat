-- @testpoint: opengauss关键字message_text(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists message_text;
create synonym message_text for explain_test;
insert into message_text values (1,'ada'),(2, 'bob');
update message_text set message_text.name='cici' where message_text.id=2;
select * from message_text;

--关键字带双引号-成功
drop synonym if exists "message_text";
create synonym "message_text" for explain_test;


--关键字带单引号-合理报错
drop synonym if exists 'message_text';
create synonym 'message_text' for explain_test;
insert into 'message_text' values (1,'ada'),(2, 'bob');
update 'message_text' set 'message_text'.name='cici' where 'message_text'.id=2;
select * from 'message_text';

--关键字带反引号-合理报错
drop synonym if exists `message_text`;
create synonym `message_text` for explain_test;
insert into `message_text` values (1,'ada'),(2, 'bob');
update `message_text` set `message_text`.name='cici' where `message_text`.id=2;
select * from `message_text`;
--清理环境
drop synonym if exists "message_text";
drop synonym if exists message_text;
drop table if exists explain_test;