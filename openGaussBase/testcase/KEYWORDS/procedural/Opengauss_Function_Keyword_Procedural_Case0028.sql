-- @testpoint: opengauss关键字procedural(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists procedural_test;
create table procedural_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists procedural;
create synonym procedural for procedural_test;
insert into procedural values (1,'ada'),(2, 'bob');
update procedural set procedural.name='cici' where procedural.id=2;
select * from procedural;
drop synonym if exists procedural;

--关键字带双引号-成功
drop synonym if exists "procedural";
create synonym "procedural" for procedural_test;
insert into "procedural" values (1,'ada'),(2, 'bob');
update "procedural" set "procedural".name='cici' where "procedural".id=2;
select * from "procedural";
drop synonym if exists "procedural";

--关键字带单引号-合理报错
drop synonym if exists 'procedural';

--关键字带反引号-合理报错
drop synonym if exists `procedural`;
--清理环境
drop table if exists procedural_test;