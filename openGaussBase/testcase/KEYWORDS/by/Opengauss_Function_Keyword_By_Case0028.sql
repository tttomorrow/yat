-- @testpoint: opengauss关键字by(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists by_test;
create table by_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists by;
create synonym by for by_test;
insert into by values (1,'ada'),(2, 'bob');
update by set by.name='cici' where by.id=2;
select * from by;

--清理环境
drop synonym if exists by;

--关键字带双引号-成功
drop synonym if exists "by";
create synonym "by" for by_test;
insert into "by" values (1,'ada'),(2, 'bob');
update "by" set "by".name='cici' where "by".id=2;
select * from "by";

--清理环境
drop synonym if exists "by";

--关键字带单引号-合理报错
drop synonym if exists 'by';

--关键字带反引号-合理报错
drop synonym if exists `by`;
drop table if exists by_test;