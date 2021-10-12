-- @testpoint: opengauss关键字window(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists window_test;
create table window_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists window;
create synonym window for window_test;


--关键字带双引号-成功
drop synonym if exists "window";
create synonym "window" for window_test;
insert into "window" values (1,'ada'),(2, 'bob');
update "window" set "window".name='cici' where "window".id=2;
select * from "window";

--清理环境
drop synonym "window";

--关键字带单引号-合理报错
drop synonym if exists 'window';
create synonym 'window' for window_test;
insert into 'window' values (1,'ada'),(2, 'bob');
update 'window' set 'window'.name='cici' where 'window'.id=2;
select * from 'window';

--关键字带反引号-合理报错
drop synonym if exists `window`;
create synonym `window` for window_test;
insert into `window` values (1,'ada'),(2, 'bob');
update `window` set `window`.name='cici' where `window`.id=2;
select * from `window`;
drop table if exists window_test;