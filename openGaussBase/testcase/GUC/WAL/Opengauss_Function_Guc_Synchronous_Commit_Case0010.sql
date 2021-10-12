-- @testpoint: 修改参数值为无效值,合理报错
--set命令设置参数值，报错
set synchronous_commit to 'remote_apply*&^%';
set synchronous_commit to '2*&^^';
set synchronous_commit to 1234;
