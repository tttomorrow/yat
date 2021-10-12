-- @testpoint: opengauss关键字percent(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists percent_test;
create table percent_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists percent;
create synonym percent for percent_test;
insert into percent values (1,'ada'),(2, 'bob');
update percent set percent.name='cici' where percent.id=2;
select * from percent;

--关键字带双引号-成功
drop synonym if exists "percent";
create synonym "percent" for percent_test;


--关键字带单引号-合理报错
drop synonym if exists 'percent';
create synonym 'percent' for percent_test;
insert into 'percent' values (1,'ada'),(2, 'bob');
update 'percent' set 'percent'.name='cici' where 'percent'.id=2;
select * from 'percent';

--关键字带反引号-合理报错
drop synonym if exists `percent`;
create synonym `percent` for percent_test;
insert into `percent` values (1,'ada'),(2, 'bob');
update `percent` set `percent`.name='cici' where `percent`.id=2;
select * from `percent`;
--清理环境
drop synonym if exists "percent";
drop synonym if exists percent;
drop table if exists percent_test;