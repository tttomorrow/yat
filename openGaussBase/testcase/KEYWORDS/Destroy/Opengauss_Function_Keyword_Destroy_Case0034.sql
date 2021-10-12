-- @testpoint: opengauss关键字destroy(非保留)，作为游标名，部分测试点合理报错

--前置条件
drop table if exists destroy_test cascade;
create table destroy_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor destroy for select * from destroy_test order by 1;
close destroy;
end;

--关键字带双引号-成功
start transaction;
cursor "destroy" for select * from destroy_test order by 1;
close "destroy";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'destroy' for select * from destroy_test order by 1;
close 'destroy';
end;

--关键字带反引号-合理报错
start transaction;
cursor `destroy` for select * from destroy_test order by 1;
close `destroy`;
end;
drop table if exists destroy_test cascade;
