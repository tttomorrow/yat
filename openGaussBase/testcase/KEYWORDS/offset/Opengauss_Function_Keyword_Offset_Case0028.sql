-- @testpoint: opengauss关键字offset(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists offset_test;
create table offset_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists offset;
create synonym offset for offset_test;


--关键字带双引号-成功
drop synonym if exists "offset";
create synonym "offset" for offset_test;
insert into "offset" values (1,'ada'),(2, 'bob');
update "offset" set "offset".name='cici' where "offset".id=2;
select * from "offset";

--清理环境
drop synonym "offset";

--关键字带单引号-合理报错
drop synonym if exists 'offset';
create synonym 'offset' for offset_test;
insert into 'offset' values (1,'ada'),(2, 'bob');
update 'offset' set 'offset'.name='cici' where 'offset'.id=2;
select * from 'offset';

--关键字带反引号-合理报错
drop synonym if exists `offset`;
create synonym `offset` for offset_test;
insert into `offset` values (1,'ada'),(2, 'bob');
update `offset` set `offset`.name='cici' where `offset`.id=2;
select * from `offset`;
--清理环境
drop table if exists offset_test cascade;