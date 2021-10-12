--  @testpoint:opengauss关键字cluster(非保留)，作为游标名
--前置条件
drop table if exists cluster_test cascade;
create table cluster_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor cluster for select * from cluster_test order by 1;
close cluster;
end;

--关键字带双引号-成功
start transaction;
cursor "cluster" for select * from cluster_test order by 1;
close "cluster";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'cluster' for select * from cluster_test order by 1;
close 'cluster';
end;

--关键字带反引号-合理报错
start transaction;
cursor `cluster` for select * from cluster_test order by 1;
close `cluster`;
end;

--清理环境
drop table cluster_test;