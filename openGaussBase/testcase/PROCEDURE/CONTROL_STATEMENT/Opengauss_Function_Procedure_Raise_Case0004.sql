-- @describe: 存储过程中调试语句  NOTICE


CREATE OR REPLACE PROCEDURE proc_raise4(user_id in integer)
AS
BEGIN
RAISE NOTICE  'Noexistence ID --> %',user_id USING HINT = 'Please check your user ID';
END;
/

call proc_raise4(300011);
drop PROCEDURE proc_raise4;