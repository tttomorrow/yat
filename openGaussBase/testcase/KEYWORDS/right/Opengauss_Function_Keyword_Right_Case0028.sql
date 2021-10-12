-- @testpoint: opengauss关键字right(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists right_test;
create table right_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists right;
create synonym right for right_test;


--关键字带双引号-成功
drop synonym if exists "right";
create synonym "right" for right_test;
insert into "right" values (1,'ada'),(2, 'bob');
update "right" set "right".name='cici' where "right".id=2;
select * from "right";

--清理环境
drop synonym "right";

--关键字带单引号-合理报错
drop synonym if exists 'right';
create synonym 'right' for right_test;
insert into 'right' values (1,'ada'),(2, 'bob');
update 'right' set 'right'.name='cici' where 'right'.id=2;
select * from 'right';

--关键字带反引号-合理报错
drop synonym if exists `right`;
create synonym `right` for right_test;
insert into `right` values (1,'ada'),(2, 'bob');
update `right` set `right`.name='cici' where `right`.id=2;
select * from `right`;
drop table if exists right_test;