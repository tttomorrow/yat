-- @testpoint: opengauss关键字reindex(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists reindex_test;
create table reindex_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists reindex;
create synonym reindex for reindex_test;
insert into reindex values (1,'ada'),(2, 'bob');
update reindex set reindex.name='cici' where reindex.id=2;
select * from reindex;
drop synonym if exists reindex;

--关键字带双引号-成功
drop synonym if exists "reindex";
create synonym "reindex" for reindex_test;
insert into "reindex" values (1,'ada'),(2, 'bob');
update "reindex" set "reindex".name='cici' where "reindex".id=2;
select * from "reindex";
drop synonym if exists "reindex";

--关键字带单引号-合理报错
drop synonym if exists 'reindex';

--关键字带反引号-合理报错
drop synonym if exists `reindex`;
drop table if exists reindex_test;