-- @describe: 存储过程中调试语句  WARNING


CREATE OR REPLACE PROCEDURE proc_raise5(user_id in integer)
AS
BEGIN
RAISE WARNING  'Noexistence ID --> %',user_id USING HINT = 'Please check your user ID';
END;
/

call proc_raise5(300011);
drop PROCEDURE proc_raise5;