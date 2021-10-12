-- @testpoint: opengauss关键字current_path(非保留)，作为游标名，部分测试点合理报错

--前置条件
drop table if exists current_path_test cascade;
create table current_path_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor current_path for select * from current_path_test order by 1;
close current_path;
end;

--关键字带双引号-成功
start transaction;
cursor "current_path" for select * from current_path_test order by 1;
close "current_path";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'current_path' for select * from current_path_test order by 1;
close 'current_path';
end;

--关键字带反引号-合理报错
start transaction;
cursor `current_path` for select * from current_path_test order by 1;
close `current_path`;
end;
drop table if exists current_path_test cascade;
