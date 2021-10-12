-- @testpoint: opengauss关键字quote(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists quote_test;
create table quote_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists quote;
create synonym quote for quote_test;
insert into quote values (1,'ada'),(2, 'bob');
update quote set quote.name='cici' where quote.id=2;
select * from quote;
drop synonym if exists quote;

--关键字带双引号-成功
drop synonym if exists "quote";
create synonym "quote" for quote_test;
insert into "quote" values (1,'ada'),(2, 'bob');
update "quote" set "quote".name='cici' where "quote".id=2;
select * from "quote";
drop synonym if exists "quote";

--关键字带单引号-合理报错
drop synonym if exists 'quote';

--关键字带反引号-合理报错
drop synonym if exists `quote`;
--清理环境
drop table if exists quote_test;