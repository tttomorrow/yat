-- @testpoint: opengauss关键字overlaps(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists overlaps_test;
create table overlaps_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists overlaps;
create synonym overlaps for overlaps_test;


--关键字带双引号-成功
drop synonym if exists "overlaps";
create synonym "overlaps" for overlaps_test;
insert into "overlaps" values (1,'ada'),(2, 'bob');
update "overlaps" set "overlaps".name='cici' where "overlaps".id=2;
select * from "overlaps";

--清理环境
drop synonym "overlaps";

--关键字带单引号-合理报错
drop synonym if exists 'overlaps';
create synonym 'overlaps' for overlaps_test;
insert into 'overlaps' values (1,'ada'),(2, 'bob');
update 'overlaps' set 'overlaps'.name='cici' where 'overlaps'.id=2;
select * from 'overlaps';

--关键字带反引号-合理报错
drop synonym if exists `overlaps`;
create synonym `overlaps` for overlaps_test;
insert into `overlaps` values (1,'ada'),(2, 'bob');
update `overlaps` set `overlaps`.name='cici' where `overlaps`.id=2;
select * from `overlaps`;
--清理环境
drop table if exists overlaps_test cascade;