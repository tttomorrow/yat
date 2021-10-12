-- @testpoint: opengauss关键字into(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists into_test;
create table into_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists into;
create synonym into for into_test;


--关键字带双引号-成功
drop synonym if exists "into";
create synonym "into" for into_test;
insert into "into" values (1,'ada'),(2, 'bob');
update "into" set "into".name='cici' where "into".id=2;
select * from "into";

--清理环境
drop synonym "into";

--关键字带单引号-合理报错
drop synonym if exists 'into';
create synonym 'into' for into_test;
insert into 'into' values (1,'ada'),(2, 'bob');
update 'into' set 'into'.name='cici' where 'into'.id=2;
select * from 'into';

--关键字带反引号-合理报错
drop synonym if exists `into`;
create synonym `into` for into_test;
insert into `into` values (1,'ada'),(2, 'bob');
update `into` set `into`.name='cici' where `into`.id=2;
select * from `into`;
--清理环境
drop table if exists into_test cascade;