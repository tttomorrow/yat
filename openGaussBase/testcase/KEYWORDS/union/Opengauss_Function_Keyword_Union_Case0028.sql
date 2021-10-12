-- @testpoint: opengauss关键字union(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists union_test;
create table union_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists union;
create synonym union for union_test;


--关键字带双引号-成功
drop synonym if exists "union";
create synonym "union" for union_test;
insert into "union" values (1,'ada'),(2, 'bob');
update "union" set "union".name='cici' where "union".id=2;
select * from "union";
drop synonym "union";
--关键字带单引号-合理报错
drop synonym if exists 'union';
create synonym 'union' for union_test;
insert into 'union' values (1,'ada'),(2, 'bob');
update 'union' set 'union'.name='cici' where 'union'.id=2;
select * from 'union';

--关键字带反引号-合理报错
drop synonym if exists `union`;
create synonym `union` for union_test;
insert into `union` values (1,'ada'),(2, 'bob');
update `union` set `union`.name='cici' where `union`.id=2;
select * from `union`;

--清理环境
drop table if exists union_test;