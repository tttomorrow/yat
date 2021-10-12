-- @testpoint: opengauss关键字cascade(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists cascade_test;
create table cascade_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists cascade;
create synonym cascade for cascade_test;
insert into cascade values (1,'ada'),(2, 'bob');
update cascade set cascade.name='cici' where cascade.id=2;
select * from cascade;

--清理环境
drop synonym if exists cascade;

--关键字带双引号-成功
drop synonym if exists "cascade";
create synonym "cascade" for cascade_test;
insert into "cascade" values (1,'ada'),(2, 'bob');
update "cascade" set "cascade".name='cici' where "cascade".id=2;
select * from "cascade";

--清理环境
drop synonym if exists "cascade";

--关键字带单引号-合理报错
drop synonym if exists 'cascade';

--关键字带反引号-合理报错
drop synonym if exists `cascade`;
drop table if exists cascade_test;