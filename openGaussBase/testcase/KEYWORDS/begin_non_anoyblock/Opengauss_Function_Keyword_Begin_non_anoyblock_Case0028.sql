-- @testpoint: opengauss关键字begin_non_anoyblock(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists begin_non_anoyblock_test;
create table begin_non_anoyblock_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists begin_non_anoyblock;
create synonym begin_non_anoyblock for begin_non_anoyblock_test;
insert into begin_non_anoyblock values (1,'ada'),(2, 'bob');
update begin_non_anoyblock set begin_non_anoyblock.name='cici' where begin_non_anoyblock.id=2;
select * from begin_non_anoyblock;

--清理环境
drop synonym if exists begin_non_anoyblock;

--关键字带双引号-成功
drop synonym if exists "begin_non_anoyblock";
create synonym "begin_non_anoyblock" for begin_non_anoyblock_test;
insert into "begin_non_anoyblock" values (1,'ada'),(2, 'bob');
update "begin_non_anoyblock" set "begin_non_anoyblock".name='cici' where "begin_non_anoyblock".id=2;
select * from "begin_non_anoyblock";

--清理环境
drop synonym if exists "begin_non_anoyblock";

--关键字带单引号-合理报错
drop synonym if exists 'begin_non_anoyblock';

--关键字带反引号-合理报错
drop synonym if exists `begin_non_anoyblock`;
drop table if exists begin_non_anoyblock_test;