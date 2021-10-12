-- @testpoint: opengauss关键字cross(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists cross_test;
create table cross_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists cross;
create synonym cross for cross_test;


--关键字带双引号-成功
drop synonym if exists "cross";
create synonym "cross" for cross_test;
insert into "cross" values (1,'ada'),(2, 'bob');
update "cross" set "cross".name='cici' where "cross".id=2;
select * from "cross";

--清理环境
drop synonym "cross";

--关键字带单引号-合理报错
drop synonym if exists 'cross';
create synonym 'cross' for cross_test;
insert into 'cross' values (1,'ada'),(2, 'bob');
update 'cross' set 'cross'.name='cici' where 'cross'.id=2;
select * from 'cross';

--关键字带反引号-合理报错
drop synonym if exists `cross`;
create synonym `cross` for cross_test;
insert into `cross` values (1,'ada'),(2, 'bob');
update `cross` set `cross`.name='cici' where `cross`.id=2;
select * from `cross`;
drop table if exists cross_test;