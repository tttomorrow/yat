-- @testpoint: opengauss关键字nvarchar(非保留)，作为表空间名 部分测试点合理报错


--step1:关键字不带引号;expect:创建成功
drop tablespace if exists nvarchar;
create tablespace nvarchar relative LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
drop tablespace nvarchar;
 
--step2:关键字带双引号;expect:创建成功
drop tablespace if exists "nvarchar";
create tablespace "nvarChar" relative location 'hdfs_tablespace/hdfs_tablespace_1';
drop tablespace "nvarChar";

--step3:关键字带单引号;expect:合理报错
drop tablespace if exists 'nvarchar';
create tablespace 'nvarchar' relative location 'hdfs_tablespace/hdfs_tablespace_1';

--step4:关键字带反引号;expect:合理报错
drop tablespace if exists `nvarchar`;
create tablespace `nvarchar` relative locatioN 'hdfs_tablespace/hdfs_tablespace_1';

