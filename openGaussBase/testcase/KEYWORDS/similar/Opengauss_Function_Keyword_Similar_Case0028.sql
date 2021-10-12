-- @testpoint: opengauss关键字similar(保留)，作为同义词对象名，合理报错


--前置条件
drop table if exists similar_test;
create table similar_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists similar;
create synonym similar for similar_test;


--关键字带双引号-成功
drop synonym if exists "similar";
create synonym "similar" for similar_test;
insert into "similar" values (1,'ada'),(2, 'bob');
update "similar" set "similar".name='cici' where "similar".id=2;
select * from "similar";

--清理环境
drop synonym "similar";

--关键字带单引号-合理报错
drop synonym if exists 'similar';
create synonym 'similar' for similar_test;
insert into 'similar' values (1,'ada'),(2, 'bob');
update 'similar' set 'similar'.name='cici' where 'similar'.id=2;
select * from 'similar';

--关键字带反引号-合理报错
drop synonym if exists `similar`;
create synonym `similar` for similar_test;
insert into `similar` values (1,'ada'),(2, 'bob');
update `similar` set `similar`.name='cici' where `similar`.id=2;
select * from `similar`;
drop table if exists similar_test;