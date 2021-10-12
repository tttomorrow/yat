-- @testpoint: 创建同义词，无同义词连接对象，合理报错
-- @modify at: 2020-11-25
drop synonym if exists  SYN_FUN_SYN_047;
create synonym SYN_FUN_SYN_047 for;
