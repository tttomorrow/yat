-- @testpoint: opengauss关键字returned_length(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists returned_length_test;
create table returned_length_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists returned_length;
create synonym returned_length for returned_length_test;
insert into returned_length values (1,'ada'),(2, 'bob');
update returned_length set returned_length.name='cici' where returned_length.id=2;
select * from returned_length;
drop synonym if exists returned_length;

--关键字带双引号-成功
drop synonym if exists "returned_length";
create synonym "returned_length" for returned_length_test;
insert into "returned_length" values (1,'ada'),(2, 'bob');
update "returned_length" set "returned_length".name='cici' where "returned_length".id=2;
select * from "returned_length";
drop synonym if exists "returned_length";

--关键字带单引号-合理报错
drop synonym if exists 'returned_length';

--关键字带反引号-合理报错
drop synonym if exists `returned_length`;
drop table if exists returned_length_test;