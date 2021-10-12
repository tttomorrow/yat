-- @testpoint: opengauss关键字Case(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists Case_test;
create table Case_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists Case;
create synonym Case for Case_test;


--关键字带双引号-成功
drop synonym if exists "Case";
create synonym "Case" for Case_test;
insert into "Case" values (1,'ada'),(2, 'bob');
update "Case" set "Case".name='cici' where "Case".id=2;
select * from "Case";

--清理环境
drop synonym "Case";

--关键字带单引号-合理报错
drop synonym if exists 'Case';
create synonym 'Case' for Case_test;
insert into 'Case' values (1,'ada'),(2, 'bob');
update 'Case' set 'Case'.name='cici' where 'Case'.id=2;
select * from 'Case';

--关键字带反引号-合理报错
drop synonym if exists `Case`;
create synonym `Case` for Case_test;
insert into `Case` values (1,'ada'),(2, 'bob');
update `Case` set `Case`.name='cici' where `Case`.id=2;
select * from `Case`;
drop table if exists Case_test;