-- @testpoint: opengauss关键字query(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists query_test;
create table query_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists query;
create synonym query for query_test;
insert into query values (1,'ada'),(2, 'bob');
update query set query.name='cici' where query.id=2;
select * from query;
drop synonym if exists query;

--关键字带双引号-成功
drop synonym if exists "query";
create synonym "query" for query_test;
insert into "query" values (1,'ada'),(2, 'bob');
update "query" set "query".name='cici' where "query".id=2;
select * from "query";
drop synonym if exists "query";

--关键字带单引号-合理报错
drop synonym if exists 'query';

--关键字带反引号-合理报错
drop synonym if exists `query`;
--清理环境
drop table if exists query_test;