-- @testpoint: opengauss关键字disconnect(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists disconnect_test;
create table disconnect_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists disconnect;
create synonym disconnect for disconnect_test;
insert into disconnect values (1,'ada'),(2, 'bob');
update disconnect set disconnect.name='cici' where disconnect.id=2;
select * from disconnect;
drop synonym if exists disconnect;

--关键字带双引号-成功
drop synonym if exists "disconnect";
create synonym "disconnect" for disconnect_test;
drop synonym if exists "disconnect";

--关键字带单引号-合理报错
drop synonym if exists 'disconnect';
create synonym 'disconnect' for disconnect_test;
insert into 'disconnect' values (1,'ada'),(2, 'bob');
update 'disconnect' set 'disconnect'.name='cici' where 'disconnect'.id=2;
select * from 'disconnect';

--关键字带反引号-合理报错
drop synonym if exists `disconnect`;
create synonym `disconnect` for disconnect_test;
insert into `disconnect` values (1,'ada'),(2, 'bob');
update `disconnect` set `disconnect`.name='cici' where `disconnect`.id=2;
select * from `disconnect`;
drop table if exists disconnect_test;