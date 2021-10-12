-- @testpoint: opengauss关键字bit_length(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists bit_length_test;
create table bit_length_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists bit_length;
create synonym bit_length for bit_length_test;
insert into bit_length values (1,'ada'),(2, 'bob');
update bit_length set bit_length.name='cici' where bit_length.id=2;
select * from bit_length;

--清理环境
drop synonym if exists bit_length;

--关键字带双引号-成功
drop synonym if exists "bit_length";
create synonym "bit_length" for bit_length_test;
insert into "bit_length" values (1,'ada'),(2, 'bob');
update "bit_length" set "bit_length".name='cici' where "bit_length".id=2;
select * from "bit_length";

--清理环境
drop synonym if exists "bit_length";

--关键字带单引号-合理报错
drop synonym if exists 'bit_length';

--关键字带反引号-合理报错
drop synonym if exists `bit_length`;
drop table if exists bit_length_test;