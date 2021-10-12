-- @testpoint: opengauss关键字depth(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists depth_test;
create table depth_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists depth;
create synonym depth for depth_test;
insert into depth values (1,'ada'),(2, 'bob');
update depth set depth.name='cici' where depth.id=2;
select * from depth;
drop synonym if exists depth;

--关键字带双引号-成功
drop synonym if exists "depth";
create synonym "depth" for depth_test;
drop synonym if exists "depth";

--关键字带单引号-合理报错
drop synonym if exists 'depth';
create synonym 'depth' for depth_test;
insert into 'depth' values (1,'ada'),(2, 'bob');
update 'depth' set 'depth'.name='cici' where 'depth'.id=2;
select * from 'depth';

--关键字带反引号-合理报错
drop synonym if exists `depth`;
create synonym `depth` for depth_test;
insert into `depth` values (1,'ada'),(2, 'bob');
update `depth` set `depth`.name='cici' where `depth`.id=2;
select * from `depth`;
drop table if exists depth_test;