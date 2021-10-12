--  @testpoint:定义和使用列时不使用account lock，解锁lh用户
drop user if exists lh cascade;
create user lh with sysadmin password 'Xiaxia2123';
alter user lh account unlock;
drop user if exists lh cascade;