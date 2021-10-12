-- @testpoint: opengauss关键字when(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists when_test;
create table when_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists when;
create synonym when for when_test;


--关键字带双引号-成功
drop synonym if exists "when";
create synonym "when" for when_test;
insert into "when" values (1,'ada'),(2, 'bob');
update "when" set "when".name='cici' where "when".id=2;
select * from "when";

--清理环境
drop synonym "when";

--关键字带单引号-合理报错
drop synonym if exists 'when';
create synonym 'when' for when_test;
insert into 'when' values (1,'ada'),(2, 'bob');
update 'when' set 'when'.name='cici' where 'when'.id=2;
select * from 'when';

--关键字带反引号-合理报错
drop synonym if exists `when`;
create synonym `when` for when_test;
insert into `when` values (1,'ada'),(2, 'bob');
update `when` set `when`.name='cici' where `when`.id=2;
select * from `when`;
drop table if exists when_test;