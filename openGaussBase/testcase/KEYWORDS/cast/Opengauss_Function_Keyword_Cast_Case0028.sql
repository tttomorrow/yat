-- @testpoint: opengauss关键字Cast(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists Cast_test;
create table Cast_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists Cast;
create synonym Cast for Cast_test;


--关键字带双引号-成功
drop synonym if exists "Cast";
create synonym "Cast" for Cast_test;
insert into "Cast" values (1,'ada'),(2, 'bob');
update "Cast" set "Cast".name='cici' where "Cast".id=2;
select * from "Cast";

--清理环境
drop synonym "Cast";

--关键字带单引号-合理报错
drop synonym if exists 'Cast';
create synonym 'Cast' for Cast_test;
insert into 'Cast' values (1,'ada'),(2, 'bob');
update 'Cast' set 'Cast'.name='cici' where 'Cast'.id=2;
select * from 'Cast';

--关键字带反引号-合理报错
drop synonym if exists `Cast`;
create synonym `Cast` for Cast_test;
insert into `Cast` values (1,'ada'),(2, 'bob');
update `Cast` set `Cast`.name='cici' where `Cast`.id=2;
select * from `Cast`;
drop table if exists Cast_test;