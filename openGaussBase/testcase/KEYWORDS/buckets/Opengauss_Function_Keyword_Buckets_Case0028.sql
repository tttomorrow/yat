-- @testpoint: opengauss关键字Buckets(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists Buckets_test;
create table Buckets_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists Buckets;
create synonym Buckets for Buckets_test;


--关键字带双引号-成功
drop synonym if exists "Buckets";
create synonym "Buckets" for Buckets_test;
insert into "Buckets" values (1,'ada'),(2, 'bob');
update "Buckets" set "Buckets".name='cici' where "Buckets".id=2;
select * from "Buckets";

--清理环境
drop synonym "Buckets";

--关键字带单引号-合理报错
drop synonym if exists 'Buckets';
create synonym 'Buckets' for Buckets_test;
insert into 'Buckets' values (1,'ada'),(2, 'bob');
update 'Buckets' set 'Buckets'.name='cici' where 'Buckets'.id=2;
select * from 'Buckets';

--关键字带反引号-合理报错
drop synonym if exists `Buckets`;
create synonym `Buckets` for Buckets_test;
insert into `Buckets` values (1,'ada'),(2, 'bob');
update `Buckets` set `Buckets`.name='cici' where `Buckets`.id=2;
select * from `Buckets`;
drop table if exists Buckets_test;