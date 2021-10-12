-- @testpoint: opengauss关键字document(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists document_test;
create table document_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists document;
create synonym document for document_test;
insert into document values (1,'ada'),(2, 'bob');
update document set document.name='cici' where document.id=2;
select * from document;
drop synonym if exists document;

--关键字带双引号-成功
drop synonym if exists "document";
create synonym "document" for document_test;
drop synonym if exists "document";

--关键字带单引号-合理报错
drop synonym if exists 'document';
create synonym 'document' for document_test;
insert into 'document' values (1,'ada'),(2, 'bob');
update 'document' set 'document'.name='cici' where 'document'.id=2;
select * from 'document';

--关键字带反引号-合理报错
drop synonym if exists `document`;
create synonym `document` for document_test;
insert into `document` values (1,'ada'),(2, 'bob');
update `document` set `document`.name='cici' where `document`.id=2;
select * from `document`;
drop table if exists document_test;