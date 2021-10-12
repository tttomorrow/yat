-- @testpoint: opengauss关键字end-exec(非保留)，作为游标名 带单引号、反引号时 合理报错

--前置条件
drop table if exists test cascade;
create table test(cid int,fid int);

--关键字不带引号-合理报错
start transaction;
cursor end-exec for select * from test order by 1;
close end-exec;
end;

--关键字带双引号-合理报错
start transaction;
cursor "end-exec" for select * from test order by 1;
close "end-exec";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'end-exec' for select * from test order by 1;
close 'end-exec';
end;

--关键字带反引号-合理报错
start transaction;
cursor `end-exec` for select * from test order by 1;
close `end-exec`;
end;

--清理环境
drop table if exists test cascade;