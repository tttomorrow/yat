-- @describe: 存储过程中调试语句  SQLSTATE


CREATE OR REPLACE PROCEDURE proc_raise7(user_id in integer)
AS
BEGIN
RAISE  info 'Duplicate user ID: %',user_id USING ERRCODE = 'unique_violation';
END;
/


call proc_raise7(300011);
drop PROCEDURE proc_raise7;

