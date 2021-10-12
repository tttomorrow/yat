-- @testpoint: opengauss关键字fetch(保留)，作为游标名，部分测试点合理报错

--前置条件
drop table if exists fetch_test cascade;
create table fetch_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor fetch for select * from fetch_test order by 1;
close fetch;
end;

--关键字带双引号-成功
start transaction;
cursor "fetch" for select * from fetch_test order by 1;
close "fetch";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'fetch' for select * from fetch_test order by 1;
close 'fetch';
end;

--关键字带反引号-合理报错
start transaction;
cursor `fetch` for select * from fetch_test order by 1;
close `fetch`;
end;
drop table if exists fetch_test cascade;
