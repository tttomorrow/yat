-- @testpoint: opengauss关键字preceding(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists preceding_test;
create table preceding_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists preceding;
create synonym preceding for preceding_test;
insert into preceding values (1,'ada'),(2, 'bob');
update preceding set preceding.name='cici' where preceding.id=2;
select * from preceding;

--关键字带双引号-成功
drop synonym if exists "preceding";
create synonym "preceding" for preceding_test;
insert into "preceding" values (1,'ada'),(2, 'bob');
update "preceding" set "preceding".name='cici' where "preceding".id=2;
select * from "preceding";

--关键字带单引号-合理报错
drop synonym if exists 'preceding';
create synonym 'preceding' for preceding_test;

--关键字带反引号-合理报错
drop synonym if exists `preceding`;
create synonym `preceding` for preceding_test;
--清理环境
drop synonym if exists "preceding";
drop synonym if exists preceding;
drop table if exists preceding_test;
