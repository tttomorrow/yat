-- @testpoint: opengauss关键字final(非保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists final_test;
create table final_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists final;
create synonym final for final_test;
insert into final values (1,'ada'),(2, 'bob');
update final set final.name='cici' where final.id=2;
select * from final;
drop synonym if exists final;

--关键字带双引号-成功
drop synonym if exists "final";
create synonym "final" for final_test;
drop synonym if exists "final";

--关键字带单引号-合理报错
drop synonym if exists 'final';
create synonym 'final' for final_test;
insert into 'final' values (1,'ada'),(2, 'bob');
update 'final' set 'final'.name='cici' where 'final'.id=2;
select * from 'final';

--关键字带反引号-合理报错
drop synonym if exists `final`;
create synonym `final` for final_test;
insert into `final` values (1,'ada'),(2, 'bob');
update `final` set `final`.name='cici' where `final`.id=2;
select * from `final`;
drop table if exists final_test;