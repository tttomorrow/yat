-- @testpoint: opengauss关键字nlssort(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists nlssort_test;
create table nlssort_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists nlssort;
create synonym nlssort for nlssort_test;


--关键字带双引号-成功
drop synonym if exists "nlssort";
create synonym "nlssort" for nlssort_test;
insert into "nlssort" values (1,'ada'),(2, 'bob');
update "nlssort" set "nlssort".name='cici' where "nlssort".id=2;
select * from "nlssort";

--清理环境
drop synonym "nlssort";

--关键字带单引号-合理报错
drop synonym if exists 'nlssort';
create synonym 'nlssort' for nlssort_test;
insert into 'nlssort' values (1,'ada'),(2, 'bob');
update 'nlssort' set 'nlssort'.name='cici' where 'nlssort'.id=2;
select * from 'nlssort';

--关键字带反引号-合理报错
drop synonym if exists `nlssort`;
create synonym `nlssort` for nlssort_test;
insert into `nlssort` values (1,'ada'),(2, 'bob');
update `nlssort` set `nlssort`.name='cici' where `nlssort`.id=2;
select * from `nlssort`;
--清理环境
drop synonym if exists "next";
drop table if exists explain_test;