-- @testpoint: opengauss关键字left(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists left_test;
create table left_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists left;
create synonym left for left_test;


--关键字带双引号-成功
drop synonym if exists "left";
create synonym "left" for left_test;
insert into "left" values (1,'ada'),(2, 'bob');
update "left" set "left".name='cici' where "left".id=2;
select * from "left";

--清理环境
drop synonym "left";

--关键字带单引号-合理报错
drop synonym if exists 'left';
create synonym 'left' for left_test;
insert into 'left' values (1,'ada'),(2, 'bob');
update 'left' set 'left'.name='cici' where 'left'.id=2;
select * from 'left';

--关键字带反引号-合理报错
drop synonym if exists `left`;
create synonym `left` for left_test;
insert into `left` values (1,'ada'),(2, 'bob');
update `left` set `left`.name='cici' where `left`.id=2;
select * from `left`;
--清理环境
drop table if exists left_test cascade;