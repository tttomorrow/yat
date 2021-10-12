-- @testpoint: opengauss关键字message_octet_length(非保留)，作为同义词对象名 合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists message_octet_length;
create synonym message_octet_length for explain_test;
insert into message_octet_length values (1,'ada'),(2, 'bob');
update message_octet_length set message_octet_length.name='cici' where message_octet_length.id=2;
select * from message_octet_length;

--关键字带双引号-成功
drop synonym if exists "message_octet_length";
create synonym "message_octet_length" for explain_test;


--关键字带单引号-合理报错
drop synonym if exists 'message_octet_length';
create synonym 'message_octet_length' for explain_test;
insert into 'message_octet_length' values (1,'ada'),(2, 'bob');
update 'message_octet_length' set 'message_octet_length'.name='cici' where 'message_octet_length'.id=2;
select * from 'message_octet_length';

--关键字带反引号-合理报错
drop synonym if exists `message_octet_length`;
create synonym `message_octet_length` for explain_test;
insert into `message_octet_length` values (1,'ada'),(2, 'bob');
update `message_octet_length` set `message_octet_length`.name='cici' where `message_octet_length`.id=2;
select * from `message_octet_length`;
--清理环境
drop synonym if exists "message_octet_length";
drop synonym if exists message_octet_length;
drop table if exists explain_test;
