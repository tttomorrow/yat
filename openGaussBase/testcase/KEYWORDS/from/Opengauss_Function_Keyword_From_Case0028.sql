-- @testpoint: opengauss关键字from(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists from_test;
create table from_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists from;
create synonym from for from_test;


--关键字带双引号-成功
drop synonym if exists "from";
create synonym "from" for from_test;
insert into "from" values (1,'ada'),(2, 'bob');
update "from" set "from".name='cici' where "from".id=2;
select * from "from";

--清理环境
drop synonym "from";

--关键字带单引号-合理报错
drop synonym if exists 'from';
create synonym 'from' for from_test;
insert into 'from' values (1,'ada'),(2, 'bob');
update 'from' set 'from'.name='cici' where 'from'.id=2;
select * from 'from';

--关键字带反引号-合理报错
drop synonym if exists `from`;
create synonym `from` for from_test;
insert into `from` values (1,'ada'),(2, 'bob');
update `from` set `from`.name='cici' where `from`.id=2;
select * from `from`;

--清理环境
drop table if exists from_test;