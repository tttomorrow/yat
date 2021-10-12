-- @testpoint: opengauss关键字Both(保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists Both_test;
create table Both_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists Both;
create synonym Both for Both_test;


--关键字带双引号-成功
drop synonym if exists "Both";
create synonym "Both" for Both_test;
insert into "Both" values (1,'ada'),(2, 'bob');
update "Both" set "Both".name='cici' where "Both".id=2;
select * from "Both";

--清理环境
drop synonym "Both";

--关键字带单引号-合理报错
drop synonym if exists 'Both';
create synonym 'Both' for Both_test;
insert into 'Both' values (1,'ada'),(2, 'bob');
update 'Both' set 'Both'.name='cici' where 'Both'.id=2;
select * from 'Both';

--关键字带反引号-合理报错
drop synonym if exists `Both`;
create synonym `Both` for Both_test;
insert into `Both` values (1,'ada'),(2, 'bob');
update `Both` set `Both`.name='cici' where `Both`.id=2;
select * from `Both`;
drop table if exists Both_test;