-- @testpoint: opengauss关键字All(保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists All_test;
create table All_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists All;
create synonym All for All_test;


--关键字带双引号-成功
drop synonym if exists "All";
create synonym "All" for All_test;
insert into "All" values (1,'ada'),(2, 'bob');
update "All" set "All".name='cici' where "All".id=2;
select * from "All";

--清理环境
drop synonym "All";
drop table if exists All_test;
--关键字带单引号-合理报错
drop synonym if exists 'All';
create synonym 'All' for All_test;
insert into 'All' values (1,'ada'),(2, 'bob');
update 'All' set 'All'.name='cici' where 'All'.id=2;
select * from 'All';

--关键字带反引号-合理报错
drop synonym if exists `All`;
create synonym `All` for All_test;
insert into `All` values (1,'ada'),(2, 'bob');
update `All` set `All`.name='cici' where `All`.id=2;
select * from `All`;