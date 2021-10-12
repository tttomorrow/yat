-- @testpoint: opengauss关键字references(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists references_test;
create table references_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists references;
create synonym references for references_test;


--关键字带双引号-成功
drop synonym if exists "references";
create synonym "references" for references_test;
insert into "references" values (1,'ada'),(2, 'bob');
update "references" set "references".name='cici' where "references".id=2;
select * from "references";

--清理环境
drop synonym "references";

--关键字带单引号-合理报错
drop synonym if exists 'references';
create synonym 'references' for references_test;
insert into 'references' values (1,'ada'),(2, 'bob');
update 'references' set 'references'.name='cici' where 'references'.id=2;
select * from 'references';

--关键字带反引号-合理报错
drop synonym if exists `references`;
create synonym `references` for references_test;
insert into `references` values (1,'ada'),(2, 'bob');
update `references` set `references`.name='cici' where `references`.id=2;
select * from `references`;
drop table if exists references_test;